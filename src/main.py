import pandas as pd
from resume_reader import extract_text_from_txt, extract_skills
from skill_matcher import evaluate_resumes

try:
    jobs_df = pd.read_csv('../Resume_Data/jobs.csv')
    job_roles = jobs_df['role']
    job_skills = jobs_df['skills'].tolist()

    resume_files = [
        '../Resume_Data/resumes/resume_1.txt',
        '../Resume_Data/resumes/resume_2.txt',
        '../Resume_Data/resumes/resume_3.txt'
    ]

    evaluate_resumes(resume_files, job_skills, extract_text_from_txt, extract_skills, job_roles)
except FileNotFoundError:
    print("Error: jobs.csv not found in Resume_Data directory")
except Exception as e:
    print(f"Unexpected error in main program: {e}")