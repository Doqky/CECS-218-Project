import re
from docx import Document  # type: ignore

def extract_text_from_docx(file_path):
    """
    Extracts text from a .docx (Word) file.

    Args:
        file_path (str): Path to the .docx file.

    Returns:
        str: Combined text from all paragraphs in the document.
    """

    try:
        doc = Document(file_path)  # Load the docx file
        text = ""
        for para in doc.paragraphs: 
            text += para.text + "\n"
        return text
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading DOCX file {file_path}: {e}")
        return ""

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
        all_skills = list(set(' '.join(job_skills_list).lower().split()))
        text_words = set(re.findall(r'\b\w[\w+.]*\b', text.lower()))
        matched_skills = [skill for skill in all_skills if skill in text_words]
        return matched_skills
    
    except Exception as e:
        print(f"Error extracting skills: {e}")
