
def prompt_for_one_stage_license_matching(comments : str) -> str:
  return f"""
    [Task]
    Carefully analyze the provided text to determine if it contains any software licenses.

    [Guidelines]
    1.  **License Identification:** If a license is found, clearly state its name and its corresponding SPDX identifier (e.g., MIT License, SPDX-License-Identifier: MIT).
    2.  **Evidence Extraction:** For each identified license, extract the specific text snippet(s) from the provided text that confirm its presence. Include surrounding context if it helps clarify the license's applicability.
    3.  **No License Scenario:** If no license is detected in the text, explicitly state "No software license found."
    4.  **Response Format:** Provide the results in the following format:
        *   **Licenses = [list of identified licenses]** 
        *   **SPDX-IDs = [list of corresponding SPDX identifiers]**

        If no licenses are found, both lists should be empty:

        *   **Licenses = []**
        *   **SPDX-IDs = []** 

    [Text]
    {comments}
    """

def prompt_for_license_text_identification(comments : str, comments_extracted: bool) -> str:
  return f"""
  Task: License Identification in Code Comments or Plain Text

  Objective:
  Extract the contiguous block (chunk) of text that is most likely to contain license-related information.

  Input:
      Either:
      1. Comment text extracted from a code file (e.g., comments from a .cpp or .py file).
      2. The full text of a file that does not typically contain comments (e.g., a NOTICE file).

  Guidelines:

  * IF COMMENT TEXT IS PROVIDED:
      * License information is typically contained within a single block of comment text.
      * License text often uses keywords like "copyright," "license," "permission," "terms," "distribution," "use," "modification," "attribution," etc.
      * License text might contain specific phrases like "All rights reserved," "MIT License," "Apache License 2.0," etc.

  * IF PLAIN TEXT IS PROVIDED:
      * License information is likely to appear as a distinct block within the text.
      * License text is still likely to contain the same keywords and phrases as above.

  Instructions:

  1. Scan the input text for license-related keywords and phrases.
  2. Identify contiguous blocks of text that have a higher density of these keywords.
  3. Among these blocks, select the one that:
      * Contains the most specific license phrases (e.g., "MIT License," "Apache License 2.0").
      * Appears most similar to typical license language (e.g., legalistic tone, reference to rights and permissions).
      * If applicable, aligns with any known conventions for licenses within the file type (e.g., header comments in code files).
  4. If no block meets the criteria, enclose the text "No license information found." in triple backticks (```).
  5. **Crucially, preserve all original spacing, indentation, and line breaks within the selected block of text.** This includes:
      * Empty lines between paragraphs
      * Leading spaces or tabs for indentation
      * Newline characters (\n) at the end of each line
  6. Enclose the selected block of text (or the "No license information found." message) within triple backticks (```) and return this as the output. 

  Additional Considerations:

  * Be mindful of false positives (e.g., discussions about licenses, legal notices, etc., that are not the actual license text).
  * Consider the length of the block. License text can vary in length, but extremely short or overly long blocks might be less likely.
  * If the input is from a code file's comments, prioritize blocks near the beginning of the file, as licenses are often placed there.

  Output:

  A single contiguous block of text representing the most likely license information, or "No license information found."

  {'File Comments:' if comments_extracted else 'File Text:'}
  {comments}
  """


def prompt_for_obligation_clause_verification(license_text : str, license_obligations : str) -> str:
  return f"""
  [Task]
  Evaluate the accuracy of each clause within the provided set of obligations against the given open-source license text. Determine if each clause is valid (supported by the license), invalid (contradicts the license), or partially valid (partially accurate or open to interpretation).

  [Instructions]
    1. Carefully analyze the open-source license text.
    2. Examine each clause within the provided obligations.
    3. Compare each clause to the relevant sections of the license text.
    4. Categorize each clause as valid, invalid, or partially valid.
    5. Provide a clear explanation for each assessment, citing specific license text sections and any interpretations.
    6. Present your analysis in the following list format only, without any additional text or commentary:
      Clause: [Clause text]
      Result: [valid/invalid/partially valid]
      Explanation: [Your detailed explanation, citing specific license text sections and any relevant interpretations]
    7. Be Concise and only follow the output format provided in Instruction 6 without any introductions or conclusions
  
  [Additional Notes]
    1. if a clause contains multiple parts, assess each part separately and then as a whole.
    2. Be concise yet thorough in your explanations.
    3. Use clear, unambiguous language.
    4. Maintain a professional, objective tone.
  
  [License Text]
  {license_text}

  [Corresponding Obligations]
  {license_obligations}
  """


def prompt_for_license_compatibility_through_obligations(license_a_obligations : str, license_b_obligations : str) -> str:
  return f"""
  [Task]
  Analyze the obligations imposed on licensees by the two license texts provided below. Consider the following key aspects:

  1.  **Attribution:**
    *   Do the licenses require attribution of the original author(s)? If so, what specific information must be included, and in what format?
    *   Are there any restrictions on how the attribution can be presented (e.g., size, placement)?

  2.  **Copyleft/ShareAlike:**
    *   Do the licenses include copyleft or ShareAlike provisions? If so, what obligations do these impose on the distribution of derivative works?
    *   Are there any exceptions or exemptions to the copyleft/ShareAlike requirements?

  3.  **Modification and Distribution:**
    *   Do the licenses allow modification of the software? If so, are there any conditions or restrictions on how the modified software can be distributed?
    *   Are there any requirements for the disclosure of source code or changes made to the software?

  4.  **Commercial Use:**
    *   Do the licenses explicitly permit or restrict commercial use of the software?
    *   If commercial use is permitted, are there any specific obligations or limitations associated with it?

  5.  **Patent Grants:**
    *   Do the licenses include any patent grants or licenses? If so, what rights do they grant, and under what conditions?

  6.  **Liability and Warranty Disclaimers:**
    *   Do the licenses include disclaimers of liability or warranty? If so, what are the specific terms and limitations of these disclaimers?

  7.  **Additional Considerations:**
    *   Are there any other important factors, provisions, or obligations in either license that may affect the analysis? This may include compatibility with other licenses, jurisdictional considerations, or any unique clauses not covered above.
    *   How might these additional considerations impact compliance or introduce challenges when working with the two licenses?

  Based on your analysis, provide a comprehensive summary of the obligations imposed by each license. Highlight any potential conflicts or ambiguities between the obligations of the two licenses.

  Overall Verdict:

  Based on the analysis above, provide an overall verdict on the relationship between the obligations of the two licenses. Are the obligations generally compatible, or are there significant conflicts that would make it difficult or impossible to comply with both licenses simultaneously? Briefly explain the reasoning behind your verdict.

  License Obligations A: 
  {license_a_obligations}

  License Obligations B:
  {license_b_obligations}
  """