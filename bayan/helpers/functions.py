import os
import json
from typing import List, Optional
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import nirjas

def sample_by_label_limit(df: pd.DataFrame, label_column: str, max_samples_per_label = 5, random_state=None):
    """
    Samples a DataFrame to ensure each unique label appears at most 
    a specified number of times, with control over random sampling.

    Args:
        df: The DataFrame to sample.
        label_column: The name of the column containing the labels.
        max_samples_per_label: The maximum number of samples per label.
        random_state: Seed for the random number generator (for reproducibility).

    Returns:
        A new DataFrame containing the sampled rows.
    """

    sampled_df = pd.DataFrame()
    for label in df[label_column].unique():
        label_df = df[df[label_column] == label]
        sample_size = min(len(label_df), max_samples_per_label) 
        sampled_df = pd.concat([sampled_df, label_df.sample(sample_size, random_state=random_state)])  # Apply random state here
    sampled_df['old_index'] = sampled_df.index
    sampled_df.reset_index(drop=True, inplace=True)
    return sampled_df

def read_json_file(file_path):

    """
    Reads and parses a JSON file into a Python dictionary.

    Args:
        file_path (str): The path to the JSON file to be read.

    Returns:
        dict or None: If successful, returns the parsed JSON data as a Python dictionary. 
                      If the file is not found or the JSON format is invalid, returns None and prints an error message.
    """

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{file_path}' - {e}")

    return None

def create_license_dataset(path_to_license_details_directory : str, output_path : Optional[str] = None):
    """
    Creates a text file containing license information (name, ID, text) from a directory of JSON license details.

    Args:
        path_to_license_details_directory (str): The path to the directory containing the license details JSON files.
        output_path (str, optional): The path to the output text file. If None, the file will be saved in the same 
                                     parent directory containing the license details.

    Raises:
        FileNotFoundError: If the specified license details directory does not exist.

    Returns:
        None: The function writes the license dataset to a file and does not return a value.
    """

    # ! The 'details' folder containing all the license details can be found at:
        # ! https://github.com/spdx/license-list-data/tree/main/json
        # ! Make sure to download the entire 'details' directory

    # Determine output file path
    if not os.path.exists(path_to_license_details_directory):
        raise FileNotFoundError(f"Directory '{path_to_license_details_directory}' not found.")

    license_dataset_file_data = []
    licenses = os.listdir(path_to_license_details_directory)

    # Determine output file path
    if output_path is None:
        parent_dir = os.path.dirname(path_to_license_details_directory)
        license_dataset_file_path = os.path.join(parent_dir, "license_dataset.csv")
    else:
        license_dataset_file_path = output_path

    # Iterate over license files and extract data
    for license in licenses:
        license_path = os.path.join(path_to_license_details_directory, license)
        with open(license_path, 'r') as file:
            license_data = json.load(file)

        license_dataset_file_data.append({
            "licenseName": license_data.get('name', ''),  # Use .get() to avoid KeyError if 'name' is missing
            "licenseId": license_data.get('licenseId', ''),
            "licenseText": license_data.get('licenseText', '')
        })

    # Write the license dataset to the output csv file
    df = pd.DataFrame(columns=['License Name', 'License ID', 'License Text'])
    
    for index, license_data in enumerate(license_dataset_file_data):
        new_row = pd.DataFrame({'License Name': f"{license_data['licenseName']}", 
                       'License ID': f"{license_data['licenseId']}",
                    #    'License Text': f"\n{license_data['licenseText']}"}, index=[index])
                       'License Text': f"\nSPDX-License-Identifier: {license_data['licenseId']}\n\nLicense Name: {license_data['licenseName']}\n\n{license_data['licenseText']}"}, index=[index])
        df = pd.concat([df, new_row], ignore_index=True)
        
    df.to_csv(license_dataset_file_path)

    print(f'License dataset file created successfully at {license_dataset_file_path}')

def extract_comments(df: pd.DataFrame):

    """
    Extracts comments from files listed in a DataFrame and adds the extracted comments 
    and a flag indicating comment extraction success to the DataFrame

    Args:
        df (pd.DataFrame): The input DataFrame, expected to have a 'file_path' column containing paths to the files

    Returns:
        pd.DataFrame: The modified DataFrame with two new columns
            'file_comments': Contains the extracted comments from each file, or the entire file content 
                             if comment extraction fails
            'comments_extracted': A boolean flag indicating whether comments were successfully extracted (True) or not (False)
    """

    for index, row in df.iterrows():
        comments_extracted = False
        try: 
            nirjas_comments = nirjas.extract(row['file_path'])
            if nirjas_comments.total_lines_of_comments == 0:
                raise Exception() # Go to the except case to read all the file, even if it has no comments
            all_comments = []
            with open(row['file_path'], "r") as f:
                all_lines = f.readlines()
            for single_line_comment in nirjas_comments['single_line_comment']:
                all_comments.append(single_line_comment['comment'])
            for cont_single_line_comment in nirjas_comments['cont_single_line_comment']:
                start = cont_single_line_comment['start_line'] - 1
                end = cont_single_line_comment['end_line']
                for line_idx in range(start, end):
                    comment = all_lines[line_idx]
                    all_comments.append(comment)
            for multi_line_comment in nirjas_comments['multi_line_comment']:
                start = multi_line_comment['start_line'] - 1
                end = multi_line_comment['end_line']
                for line_idx in range(start, end):
                    line = all_lines[line_idx]
                    all_comments.append(line) 
            comments = "".join(all_comments)
            comments_extracted = True
        except:
            with open(row['file_path'], "r") as f:
                comments = f.read()
        df.loc[index, 'file_comments'] = comments
        df.loc[index, 'comments_extracted'] = comments_extracted
    return df

def scan(file_comments : List[str], licenseList : pd.DataFrame): 
    '''
    Scans a file's comments for potential licenses using semantic search and fuzzy string matching.

    Args:
        file_comments (list): A list of strings representing the comments extracted from a file
        licenseList (pd.DataFrame): A DataFrame containing license information, including 'fullname', 'shortname', 'text', and optionally 'license_header'

    Returns:
        list: A list of dictionaries, each representing a potential license match. Each dictionary contains:
            'shortname': The short name of the matched license
            'sim_score': The similarity score of the match
            'sim_type': The type of similarity used for the match ("SemanticSearch-LVD")
            'description': An empty string (presumably for future use)
    '''

    assert 'fullname' in licenseList.columns, "licenseList must have a 'fullname' column"
    assert 'shortname' in licenseList.columns, "licenseList must have a 'shortname' column"
    assert 'text' in licenseList.columns, "licenseList must have a 'text' column"

    # Append The Fulll License Name, Short License Name, and SPDX-License-Identifier to the license text
    # Some files only contain 'SPDX-License-Identifier: 0BSD' or 'License: 0BSD' and since this agent attempts
    # To match based on license text matching, those will not be identified. Appending those lines
    # To the license text helps this agent identify those cases more often
    def convert(row):
        row['text'] = f"License Name: {row['fullname']} \n License: {row['shortname']} \n SPDX-License-Identifier: {row['shortname']} \n{row['text']}"
        return row
    
    licenseList = licenseList.apply(convert, axis=1)

    # Remove characters not found in license texts
    chars_to_remove = ['—', '…', '•', '§', '«', '»', '„', '・', '−', '*', '>', '<']
    for char_to_remove in chars_to_remove:
        file_comments = file_comments.replace(char_to_remove, '')

    # Separate the comments into single line comments
    file_comments = file_comments.split('\n')

    # Separate each license text line by line and append them to one big list (used for matching)
    # The license_index_map maps each line to the correct license index in the licenseList dataframe
    license_index_map = {}
    all_license_texts = []
    for license_index, license_text in enumerate(licenseList['text']):
        for line in license_text.split('\n'):
            all_license_texts.append(line)
            license_index_map[len(all_license_texts) - 1] = license_index
    
    # Perform first level fuzzy matching for all lines in the comments
    results = []
    fuzzy_similarity_matrix = np.zeros((len(file_comments), len(all_license_texts)))
    for index, comment in enumerate(file_comments):
        for i in range(len(all_license_texts)):
            fuzzy_similarity_matrix[index][i] = fuzz.ratio(comment, all_license_texts[i]) 
        max_score_index = np.argmax(fuzzy_similarity_matrix[index]) 
        results.append(
                    (
                        fuzzy_similarity_matrix[index][max_score_index], 
                        comment
                    )
                ) 
    
    # Try to append lines that match with a similarity score of more than 40% with one of the lines in 
    # Any of the licenses. The goal is to get a bigger and bigger text chunk that matches to a bigger 
    # text chunk in one of the license texts - The bigger the chunk, the more likely that this match is 
    # correct.
    appended_comments = []
    appended_comment = []
    for result in results:
        if result[0] >= 40:
            if appended_comment == [] and result[1] == '':
                continue
            appended_comment.append(result[1])
        else:
            appended_comments.append(appended_comment)
            appended_comment = []
    
    if len(appended_comment) > 0 and appended_comment not in appended_comments:
        appended_comments.append(appended_comment)

    # Attempt the final - second level license match with all the bigger text chunks
    # In some licenses, the license header is used instead of the license text
    # In case that a license has a license header, we match all chunks with both and take 
    # the match with the highest similarity score
    results = []
    for appended_comment in appended_comments:
        appended_comment = "\n".join(appended_comment)
        fuzzy_similarity_matrix_2 = np.zeros(len(licenseList))
        for i in range(len(licenseList)):
            fuzzy_similarity_matrix_2[i] = fuzz.ratio(appended_comment, licenseList.loc[i, 'text'])
            if pd.notna(licenseList.loc[i, 'license_header']):
                license_header_sim_score = fuzz.ratio(appended_comment, licenseList.loc[i, 'license_header'].replace('\n\n', '\n'))
                fuzzy_similarity_matrix_2[i] = license_header_sim_score if license_header_sim_score > fuzzy_similarity_matrix_2[i] else fuzzy_similarity_matrix_2[i]
        top_5_license_text_indices = np.argsort(fuzzy_similarity_matrix_2)[-5:][::-1]
    
        if fuzzy_similarity_matrix_2[top_5_license_text_indices[0]] >= 50:
            results.append({
            "shortname": licenseList.loc[top_5_license_text_indices[0], 'shortname'],
            "sim_score": fuzzy_similarity_matrix_2[top_5_license_text_indices[0]],
            "sim_type": "SemanticSearch-LVD",
            "description": ""
            })
    return results

# ? Deprecated functions, used for evaluation of early iterations of semantic search ?

def license_line_found(top_k_lines, relevant_lines):
    top_k_lines = top_k_lines.split('\n')
    relevant_lines = relevant_lines[2:-2].split("', '")

    if relevant_lines[0] == '':
        return 1

    for line in relevant_lines:
        for top_line in top_k_lines:
            similarity_ratio = fuzz.ratio(line, top_line)  
            if similarity_ratio >= 80:
                return 1
    return 0

def asses_coverage(top_k_lines, relevant_lines):
    top_k_lines = top_k_lines.split('\n')
    relevant_lines = relevant_lines[2:-2].split("', '")
    
    coverage = 100

    if relevant_lines[0] == '':
        return coverage

    for line in relevant_lines:
        covered = False
        for top_line in top_k_lines:
            similarity_ratio = fuzz.ratio(line, top_line)  
            if similarity_ratio >= 80:
                covered = True
        if not covered:
            coverage -= (1 / len(relevant_lines)) * 100
    return coverage

def predicted_license_found(license_ids, labels):
    labels = labels.split(' ')
    license_ids = license_ids.split('\n')

    if labels[0] == 'No_license_found':
        return 1

    for label in labels:
        for license_id in license_ids:
            similarity_ratio = fuzz.ratio(label, license_id)  
            if (similarity_ratio >= 35) or label in license_id:
                return 1
    return 0

def predicted_license_covered(license_ids, labels):
    labels = labels.split(' ')
    license_ids = license_ids.split('\n')

    if labels[0] == 'No_license_found':
        return 100

    coverage = 100

    for label in labels:
        covered = False
        for license_id in license_ids:
            similarity_ratio = fuzz.ratio(label, license_id)  
            if similarity_ratio >= 40:
                covered = True
        if not covered:
            coverage -= (1 / len(labels)) * 100
    return coverage