import re

def extract_text_from_txt(file_path): 
    """
    Extracts text from a .txt file.

    Args:
        file_path (str): Path to the .txt file.

    Returns:
        str: Extracted text from the file.

    """

    try:
        with open(file_path, 'r') as file: # Open the file in read mode
            return file.read() # Read the content of the file and return it as a string
        
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

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
