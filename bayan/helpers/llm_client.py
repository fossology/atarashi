from typing import Callable
from typing import Optional
from loguru import logger
from openai import OpenAI
from langchain_groq import ChatGroq
import pandas as pd
import os
import shutil
import random
import string
import time
from tenacity import retry, stop_after_attempt, wait_random_exponential
from ratelimit import limits
from helpers.models import Models
from helpers.functions import extract_comments
import tiktoken
from helpers.prompts import *

class LLMClient():
    """
    This class provides a unified interface for interacting with various Large Language Models (LLMs)
    from different providers (Groq, NVIDIA, Together AI). It handles rate limiting, retries,
    and error logging for reliable inference.

    Supported Models:
        - Llama 3 8b (Groq)
        - Mistral 7b (Together AI)
        - Phi 3 mini, small, medium, Gemma 2 9b (NVIDIA)
        - Gemma 1 7b (Groq)
    """

    def __init__(self):
        """
        Initializes clients for all supported LLM models. Requires the API keys to be environment variables
        """
        
        # Groq clients (separate clients for each model due to Groq's current limitations)
        self.llama3_8b_client = ChatGroq(
            groq_api_key = os.getenv('GROQ_API_KEY'),
            model =  Models.LLAMA_3_8b.value
        )

        self.llama3_1_8b_client = ChatGroq(
            groq_api_key = os.getenv('GROQ_API_KEY'),
            model =  Models.LLAMA_3_1_8b.value
        )

        self.gemma_7b_client = ChatGroq(
            groq_api_key = os.getenv('GROQ_API_KEY'),
            model = Models.GEMMA_7b.value 
        )

        self.gemma_2_9b_client = ChatGroq(
            groq_api_key = os.getenv('GROQ_API_KEY'),
            model = Models.GEMMA_2_9b.value 
        )

        self.nvidiaClient = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key= os.getenv('NVIDIA_API_KEY'),
        )

        self.togetherClient = OpenAI(
            base_url='https://api.together.xyz/v1',
            api_key=os.getenv('TOGETHER_API_KEY'),
        )

        # Generate a random ID for logging
        self.random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        self.error_log_file_name = os.path.join('logs', f"logs_{self.random_id}.log")
        
        # Configure logger
        logger.add(self.error_log_file_name)
        self.logger = logger

    def _get_rate_limit(self, model: Models):
        """
        Gets the rate limit (requests per minute) for a given model.

        Args:
            model: The LLM model.

        Returns:
            The rate limit as an integer.

        Raises:
            Exception: If the model is not recognized.
        """

        # Rate limits are defined based on model groups
        if model.name in [Models.LLAMA_3_8b.name, Models.GEMMA_7b.name, 
                          Models.LLAMA_3_1_8b.name, Models.GEMMA_2_9b.name]:
            return 28
        elif model.name in [Models.MISTRAL_7b.name, Models.TOGETHER_GEMMA_2_9b.name]:
            return 58
        elif model.name in [Models.PHI_3_MINI.name, Models.PHI_3_SMALL.name,
                            Models.PHI_3_MEDIUM.name]:
            return 55
        else:
            raise Exception(f'Unrecognized model: {model.name}')
    
    def _get_context_window_size(self, model: Models):
        """
        Gets the context window size (maximum number of tokens the model can handle) for a given model.

        Args:
            model: The LLM model.

        Returns:
            The context window size as an integer.

        Raises:
            Exception: If the model is not recognized.
        """
        
        if model.name in [Models.LLAMA_3_8b.name, Models.GEMMA_7b.name, 
                          Models.GEMMA_2_9b.name]:
            return 8192
        elif model.name in [Models.LLAMA_3_1_8b.name]:
            return 131072
        elif model.name in [Models.MISTRAL_7b.name, Models.TOGETHER_GEMMA_2_9b.name]:
            return 8192
        elif model.name in [Models.PHI_3_MINI.name, Models.PHI_3_SMALL.name,
                            Models.PHI_3_MEDIUM.name]:
            return 128000
        else:
            raise Exception(f'Unrecognized model: {model.name}')
    
    def _infer(self, model : Models, prompt : str, temperature : float = 0):
        """
        Performs inference with the specified LLM model, handling retries and rate limiting.

        Args:
            model: The LLM model to use.
            prompt: The text prompt for the model.
            temperature: The sampling temperature (0 for deterministic output).

        Returns:
            The model's response text.

        Raises:
            Exception: If the prompt exceeds 95% of the model's context window or if the model is not recognized.
        """

        rate_limit = self._get_rate_limit(model)
        context_window_size = self._get_context_window_size(model)
        
        # Estimate the number of tokens in the prompt
        encoding = "cl100k_base"
        tokenizer = tiktoken.get_encoding(encoding)
        number_of_prompt_tokens = len(tokenizer.encode(prompt))

        # Check if the prompt is too long for the model's context window
        if number_of_prompt_tokens >= 0.95 * context_window_size:
            raise Exception(f"The estimated number of tokens for the current prompt is: {number_of_prompt_tokens}, "
                            f"while the current context window is {context_window_size}. Skipping this prompt")

        # Define an internal function with retry and rate limiting decorators
        @retry(reraise=True, wait=wait_random_exponential(min=60, max=120), stop=stop_after_attempt(5))
        @limits(calls=rate_limit, period=60)
        def _internal_func():
            # Handle inference for each supported model
            if model.name == Models.LLAMA_3_8b.name:
                self.llama3_8b_client.temperature = temperature
                response = self.llama3_8b_client.invoke(prompt).content
            elif model.name == Models.LLAMA_3_1_8b.name:
                self.llama3_1_8b_client.temperature = temperature
                response = self.llama3_1_8b_client.invoke(prompt).content
            elif model.name == Models.GEMMA_7b.name:
                self.gemma_7b_client.temperature = temperature
                response = self.gemma_7b_client.invoke(prompt).content
            elif model.name == Models.GEMMA_2_9b.name:
                self.gemma_2_9b_client.temperature = temperature
                response = self.gemma_2_9b_client.invoke(prompt).content
            elif model.name in [Models.MISTRAL_7b.name, Models.TOGETHER_GEMMA_2_9b.name]:
                chat_completion = self.togetherClient.chat.completions.create(
                    model=model.value,
                    messages=[
                        {'role': 'user', 'content': prompt}
                    ],
                    n=1,
                    temperature=temperature,
                )
                response = chat_completion.choices[0].message.content
            elif model.name in [Models.PHI_3_MINI.name, Models.PHI_3_SMALL.name,
                                Models.PHI_3_MEDIUM.name]:
                chat_completion = self.nvidiaClient.chat.completions.create(
                    model=model.value,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature if temperature != 0 else 0.01,
                    max_tokens=2024
                )
                response = chat_completion.choices[0].message.content
            else:
                raise Exception(f'Unrecognized model: {model.name}')

            return response

        # Call the internal function to perform inference
        return _internal_func()
    
    def process_dataset_for_license_text_identification(
        self, 
        df: pd.DataFrame, 
        model: Models, 
        prompt_function: Callable[[str, bool], str] = lambda x, y: prompt_for_license_text_identification(x, y), 
        output_name: Optional[str] = None, 
        output_path: str = 'results', 
        temperature: float = 0,
        log_every: int = 0, 
        retry_fails: bool = True
    ) -> pd.DataFrame :
        """
        Processes a dataset using the specified LLM model.

        Args:
            df: A Pandas DataFrame containing file paths for the files to be processed in the column 'file_path'
            model: The LLM model to use for processing.
            prompt_function: A function that generates prompts for the LLM, taking file comments and 
                             a boolean indicating if comments were extracted as input. 
                             Defaults to a lambda function that calls an external function 
                             `prompt_for_license_text_identification` to construct the prompt.
            output_name: The base name for the output CSV file. If None, a new name will be generated based on 
                         existing files in the output path.
            output_path: The directory where the output CSV file and error log will be saved. Defaults to 'results'.
            temperature: The sampling temperature for the LLM (0 for deterministic output).
            log_every: Log progress every specified number of iterations. 0 disables logging.
            retry_fails: Whether to retry failed inferences.

        Returns:
            The processed DataFrame with an additional 'response' column containing the LLM's output for each file.

        """

        # Extract comments from files if the 'file_comments' column doesn't exist
        if 'file_comments' not in df.columns:
            df = extract_comments(df)

        # Iterate over files, generate prompts, and perform inference
        for index, row in df.iterrows():
            prompt = prompt_function(row['file_comments'], row['comments_extracted'])

            # Log progress if enabled
            if log_every > 0:
                if index % log_every == 0:
                    self.logger.info(f"Processing index: {index}")  
            
            try:
                df.loc[index, 'response'] = self._infer(model, prompt, temperature)
            except Exception as e:
                self.logger.error(f"Unhandled exception at index: {index}, Exception: {e}")
        
        # Identify failed inferences
        error_indices = df[df['response'].isna()].index

        # Retry failed inferences if enabled
        if retry_fails:
            for _ in range(5):  # Maximum of 5 retry attempts
                for index in error_indices.copy():  # Copy to avoid modifying during iteration
                    prompt = prompt_function(df.loc[index, 'file_comments'], df.loc[index, 'comments_extracted'])
                    for _ in range(5):  # Maximum of 5 attempts per inference
                        try:
                            df.loc[index, 'response'] = self._infer(model, prompt, temperature)
                            self.logger.debug(f"Exception at index: {index} was retried successfully")
                            error_indices = error_indices.drop(index)  # Remove successful retry from list
                            break 
                        except Exception as e:
                            self.logger.error(f"Retry failed at index: {index}, Exception: {e}")
                            time.sleep(0.5)

        # Generate output file name if not provided
        if output_name is None:
            existing_files = [f for f in os.listdir(output_path) if os.path.isfile(os.path.join(output_path, f))]
            output_name = len(existing_files) + 1

        if not (os.path.exists(output_path) and os.path.isdir(output_path)):
            os.mkdir(output_path)

        df.to_csv(os.path.join(output_path, f'{output_name}.csv'))
        shutil.copyfile(''+self.error_log_file_name, f'{output_name}.log')
        
        # Clear the error log file
        open(''+self.error_log_file_name, 'w').close()

        # Filter out rows with missing responses (failed inferences)
        df_remaining = df[df['response'].notna()].copy()

        return df_remaining

    def process_dataset(
        self, 
        df: pd.DataFrame, 
        model: Models, 
        prompt_function: Callable[[str], str] = lambda x: x, 
        output_name: Optional[str] = None, 
        output_path='results', 
        temperature: float = 0, 
        log_every: int = 0, 
        retry_fails: bool = True
    ) -> pd.DataFrame:
        
        """
        Processes a dataset using the specified LLM model.

        Args:
            df: A Pandas DataFrame containing file paths and potentially other metadata.
            model: The LLM model to use for processing.
            prompt_function: A function that generates prompts for the LLM, taking file comments as input. 
                             Defaults to a lambda function that returns the file comments as the prompt.
            output_name: The base name for the output CSV file. If None, a new name will be generated based on 
                         existing files in the output path.
            output_path: The directory where the output CSV file and error log will be saved. Defaults to 'results'.
            temperature: The sampling temperature for the LLM (0 for deterministic output).
            log_every: Log progress every specified number of iterations. 0 disables logging.
            retry_fails: Whether to retry failed inferences.

        Returns:
            The processed DataFrame with an additional 'response' column containing the LLM's output for each file.
        """


        # Iterate over files, generate prompts, and perform inference
        for index, row in df.iterrows():
            prompt = prompt_function(row['text'])

            # Log progress if enabled
            if log_every > 0 and index % log_every == 0:
                self.logger.info(f"Processing index: {index}")

            try:
                df.loc[index, 'response'] = self._infer(model, prompt, temperature)
            except Exception as e:
                self.logger.error(f"Unhandled exception at index: {index}, Exception: {e}")

        # Identify failed inferences
        error_indices = df[df['response'].isna()].index

        # Retry failed inferences if enabled
        if retry_fails:
            for _ in range(5):  # Maximum of 5 retry attempts
                for index in error_indices.copy():  # Copy to avoid modifying during iteration
                    prompt = prompt_function(df.loc[index, 'text'])
                    for _ in range(5):  # Maximum of 5 attempts per inference
                        try:
                            df.loc[index, 'response'] = self._infer(model, prompt, temperature)
                            self.logger.debug(f"Exception at index: {index} was retried successfully")
                            error_indices = error_indices.drop(index)  # Remove successful retry from list
                            break 
                        except Exception as e:
                            self.logger.error(f"Retry failed at index: {index}, Exception: {e}")
                            time.sleep(0.5)

        # Generate output file name if not provided
        if output_name is None:
            existing_files = [f for f in os.listdir(output_path) if os.path.isfile(os.path.join(output_path, f))]
            output_name = len(existing_files) + 1

        if not (os.path.exists(output_path) and os.path.isdir(output_path)):
            os.mkdir(output_path)

        # Save the processed DataFrame and copy the error log
        df.to_csv(os.path.join(output_path, f'{output_name}.csv'))
        shutil.copyfile(''+self.error_log_file_name, f'{output_name}.log')
        
        # Clear the error log file
        open(''+self.error_log_file_name, 'w').close()

        # Filter out rows with missing responses (failed inferences)
        df_remaining = df[df['response'].notna()].copy()

        return df_remaining

    def process_dataset_for_obligation_clause_verification(
        self, 
        df: pd.DataFrame, 
        model: Models,
        prompt_function: Callable[[str, str], str] = lambda x, y : prompt_for_obligation_clause_verification(x, y), 
        output_name: Optional[str] = None, 
        output_path='results', 
        temperature: float = 0,
        log_every: int = 0, 
        retry_fails: bool = True
    ) -> pd.DataFrame:
        
        """
        Processes a dataset to identify license obligations within files, utilizing the specified LLM model.

        Args:
            df: A Pandas DataFrame containing 'License Text' and 'Obligations' columns.
            model: The LLM model to use for license obligation identification
            prompt_function: A function that generates prompts for the LLM, taking license text and
                             obligations as input.
                             Defaults to a lambda function that calls an external function 
                             `prompt_for_obligation_clause_verification` to construct the prompt.
            output_name: The base name for the output CSV file. If None, a new name will be generated based on 
                         existing files in the output path
            output_path: The directory where the output CSV file and error log will be saved. Defaults to 'results'
            temperature: The sampling temperature for the LLM (0 for deterministic output)
            log_every: Log progress every specified number of iterations. 0 disables logging
            retry_fails: Whether to retry failed inferences

        Returns:
            The processed DataFrame with an additional 'response' column containing the LLM's output for each file
        """

        # Iterate over files, generate prompts, and perform inference
        for index, row in df.iterrows():
            prompt = prompt_function(row['License Text'], row['Obligations'])

            # Log progress if enabled
            if log_every > 0:
                if index % log_every == 0:
                    self.logger.info(f"Processing index: {index}")  
            
            try:
                df.loc[index, 'response'] = self._infer(model, prompt, temperature)
            except Exception as e:
                self.logger.error(f"Unhandled exception at index: {index}, Exception: {e}")

        # Identify failed inferences
        error_indices = df[df['response'].isna()].index

        # Retry failed inferences if enabled
        if retry_fails:
            for _ in range(5):  # Maximum of 5 retry attempts
                for index in error_indices.copy():  # Copy to avoid modifying during iteration
                    prompt = prompt_function(df.loc[index, 'License Text'], df.loc[index, 'Obligations'])
                    for _ in range(5):  # Maximum of 5 attempts per inference
                        try:
                            df.loc[index, 'response'] = self._infer(model, prompt, temperature)
                            self.logger.debug(f"Exception at index: {index} was retried successfully")
                            error_indices = error_indices.drop(index)  # Remove successful retry from list
                            break 
                        except Exception as e:
                            self.logger.error(f"Retry failed at index: {index}, Exception: {e}")
                            time.sleep(0.5)

        # Generate output file name if not provided
        if output_name is None:
            existing_files = [f for f in os.listdir(output_path) if os.path.isfile(os.path.join(output_path, f))]
            output_name = len(existing_files) + 1

        if not (os.path.exists(output_path) and os.path.isdir(output_path)):
            os.mkdir(output_path)

        # Save the processed DataFrame and copy the error log
        df.to_csv(os.path.join('results', f'{output_name}.csv'))
        shutil.copyfile(''+self.error_log_file_name, f'{output_name}.log')

        # Clear the error log file
        open(''+self.error_log_file_name, 'w').close()

        return df
    