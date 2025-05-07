import pandas as pd
from resume_reader import extract_text_from_docx, extract_skills
from skill_matcher import evaluate_resumes

try:
    jobs_df = pd.read_csv('../Resume_Data/jobs.csv') # Read the CSV file containing job roles and skills in a DataFrame format
    job_roles = jobs_df['role'] # List of job roles in Series format
    job_skills = jobs_df['skills'].tolist() # List of job skills in Series format

    resume_files = [ # List of resume file paths
        '../Resume_Data/resumes/resume_1.docx',
        '../Resume_Data/resumes/resume_2.docx',
        '../Resume_Data/resumes/resume_3.docx',
        '../Resume_Data/resumes/resume_4.docx',
        '../Resume_Data/resumes/resume_5.docx',
    ]

    evaluate_resumes(resume_files, job_skills, extract_text_from_docx, extract_skills, job_roles) # This function evaluates the resumes and returns the results

except FileNotFoundError:
    print("Error: jobs.csv not found in Resume_Data directory") 
except Exception as e:
    print(f"Unexpected error in main program: {e}") 