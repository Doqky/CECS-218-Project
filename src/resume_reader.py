import re
from docx import Document

def extract_text_from_docx(file_path):
    """
    Extracts text from a .docx (Word) file.

    Args:
        file_path (str): Path to the .docx file.

    Returns:
        str: Combined text from all paragraphs in the document.
    """
    
    try:
        doc = Document(file_path)  #this is to load the docx file to access its content
        text = ""  # Initialize an empty string to store the text
        for para in doc.paragraphs: # Iterate through each paragraph in the document
            text += para.text # extract the plain text from the paragraph and append it to the text variable
        return text
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading DOCX file {file_path}: {e}")
        return ""


def extract_skills( text , job_skills_list):
    """
    Extracts skills from the given text based on a list of job skills.

    Args:
        text (str): The text from which to extract skills.
        job_skills_list (list): A list of job skills.

    Returns:
            list: A list of matched skills found in the text.

    """

    try:
        all_skills = list(set(' '.join(job_skills_list).lower().split())) #Converts the skills into a list of unique skills and lowercases them
        text_words = list(set(re.findall(r'\b\w[\w+.]*\b', text.lower()))) #Converts the text into a list of unique words and lowercases them
        matched_skills = [] # Initialize an empty list to store matched skills

        for skill in all_skills: #Iterate through the list of skills
            if skill in text_words:
                matched_skills.append(skill) #If the skill is found in the text, append it to the matched_skills list
        
        return matched_skills

    except Exception as e:
        print(f"Error extracting skills: {e}")
