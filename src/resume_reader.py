import re

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

def extract_skills( text , job_skills_list):
    try:
        all_skills = list(set(' '.join(job_skills_list).lower().split()))
        text_words = list(set(re.findall(r'\b\w[\w+.]*\b', text.lower())))
        return [skill for skill in all_skills if skill in text_words]
    except Exception as e:
        print(f"Error extracting skills: {e}")
