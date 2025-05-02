import re

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def extract_skills(text, job_skills_list):
    try:
        if job_skills_list:
            all_skills = list(set(' '.join(job_skills_list).lower().split()))
            text_words = set(re.findall(r'\b\w[\w+.-]*\b', text.lower()))
            found_skills = [skill for skill in all_skills if skill in text_words]
        
        return list(set([skill.lower() for skill in found_skills]))
    except Exception as e:
        print(f"Error extracting skills: {e}")
        return []