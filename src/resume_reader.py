import re
from docx import Document  # type: ignore

def extract_text_from_docx(file_path):
    """
    Extracts text from a .docx (Word) file.

    Args:
        file_path (str): Path to the .docx file.

    Returns:
        str: Combined text from all paragraphs in the document, or an empty string if none found.
    """

    try:
        doc = Document(file_path)  # Load the docx file
        
        text = ""
        for para in doc.paragraphs:  # Iterate through each paragraph
            if para.text: # Check if the paragraph is not empty
                text += para.text + "\n"
        return text

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error reading DOCX file {file_path}: {e}")

def extract_skills(text, job_skills_list):
    """
    Extracts skills from the given text based on a list of job skills.

    Args:
        text (str): The text from which to extract skills.
        job_skills_list (list): A list of job skills.

    Returns:
        list: A list of matched skills found in the text.
    """

    try:
        all_skills = list(set(' '.join(job_skills_list).lower().split())) # Create a set of all skills from the job_skills_list
        text_words = set(re.findall(r'\b\w[\w+.]*\b', text.lower())) # Extract words from the text
        matched_skills = []

        for skill in all_skills: # Iterate through each skill
            if skill in text_words: # Check if the skill is in the text
                matched_skills.append(skill) # If the skill is found, add it to the matched_skills list

        return matched_skills

    except Exception as e:
        print(f"Error extracting skills: {e}")
