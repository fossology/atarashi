# AI-Powered Software License Identification

This project leverages large language models (LLMs) to identify and extract relevant chunks of text pertaining to software licenses. It's a valuable tool for developers and legal teams needing to quickly pinpoint licensing information within extensive text.

## Table of Contents

- [AI-Powered Software License Identification](#ai-powered-software-license-identification)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Step 1: Install dependencies](#step-1-install-dependencies)
    - [Dependencies:](#dependencies)
  - [Setting Up API Keys:](#setting-up-api-keys)
    - [Step 1: Obtain an API Key](#step-1-obtain-an-api-key)
    - [Step 2: Set Up Environment Variables](#step-2-set-up-environment-variables)
    - [Alternative Method: Storing in .bashrc](#alternative-method-storing-in-bashrc)
  - [Basic Usage](#basic-usage)

## Installation

To run this project, you need to install the required dependencies. The project uses Python 3.8+.

### Step 1: Install dependencies

You can install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
### Dependencies:

The project relies on the following libraries:

* loguru==0.7.2
* openai==1.31.1
* pandas==2.0.3
* tenacity==8.3.0
* ratelimit==2.2.1
* Nirjas==1.0.1
* fuzzywuzzy[speedup]>=0.18.0
* langchain_groq
* tiktoken

## Setting Up API Keys:

To run the LLM models, you need to set up your API keys for the relevant services. The project primarily uses the OpenAI API for its LLM capabilities.

### Step 1: Obtain an API Key

* Visit GroQ, TogetherAI, etc. and sign up for an account if you don’t have one.

### Step 2: Set Up Environment Variables

You can add your API key to your environment variables to keep it secure:

For Linux/MacOS:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

For Windows:

```bash
set OPENAI_API_KEY='your-api-key-here'
```

Alternatively, you can create a `.env` file in the project root directory and add your API key there:

```bash
OPENAI_API_KEY=your-api-key-here
```

### Alternative Method: Storing in .bashrc
In addition to using environment variables directly, you can also store your API keys in your `.bashrc` file. This approach offers a degree of persistence, as the keys will be loaded each time you open a new terminal session.

Steps:

1. Open your `.bashrc` file using a text editor:
    ```
    sudo gedit ~/.bashrc
    ```

2. Add the following lines at the end of the file, replacing the placeholders with your actual API keys:

    ```
    # Add your own API keys here
    export GROQ_API_KEY=""
    export NVIDIA_API_KEY=""
    export TOGETHER_API_KEY=""
    ```

3. Save the file and close the text editor.

4. To apply the changes immediately, either close and reopen your terminal or run the following command:

    ```
    source ~/.bashrc
    ```

## Basic Usage

```
from helpers.llm_client import LLMClient
from helpers.models import *

client = LLMClient()

client._infer(model = Models.GEMMA_2_9b, prompt = 'Hey, How are you?', temperature = 0.1)
```

More details can be found in the [project-showcase](./project-showcase.ipynb) notebook.



