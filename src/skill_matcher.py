from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import re
import numpy as np

def build_training_data(job_skills_list):
    try:
        all_skills = list(set(' '.join(job_skills_list).lower().split()))
        job_vectors = np.array([[1 if skill in job.lower().split() else 0 for skill in all_skills] for job in job_skills_list])
        return job_vectors, all_skills
    except Exception as e:
        print(f"Error building training data: {e}")
        return np.array([]), []

def vectorize_candidate(candidate_skills, all_skills):
    try:
        return np.array([[1 if skill in candidate_skills else 0 for skill in all_skills]])
    except Exception as e:
        print(f"Error vectorizing candidate: {e}")
        return np.array([[]])


def evaluate_resumes(resume_files, job_skills_list, extract_text_func, extract_skills_func, job_roles):
    try:
        job_vectors, all_skills = build_training_data(job_skills_list)

        for i, resume_path in enumerate(resume_files):
            print("\n---------------------------")
            

            text = extract_text_func(resume_path)
            if not text:
                continue
            name_match = re.search(r'Name[:\s]*([A-Z][a-z]+\s[A-Z][a-z]+)', text)
            email_match = re.search(r'[\w.-]+@[\w.-]+', text)
            name = name_match.group(1) if name_match else "Name not found"
            email = email_match.group(0) if email_match else "Email not found"
            print(f"Processing Resume {i+1} - {name} ({email}):")
            skills = extract_skills_func(text, job_skills_list)
            print("Extracted Candidate Skills:", skills)
            if not skills:
                continue
            candidate_vector = vectorize_candidate(skills, all_skills)

            similarities = cosine_similarity(candidate_vector, job_vectors)[0]
            max_score = max(similarities)
            predicted_indices = [j for j, s in enumerate(similarities) if s == max_score]
            predicted_idx = predicted_indices[0]

            print(f"{name} ({email}) most suits the role: {job_roles.iloc[predicted_idx]}")
            for j, score in enumerate(similarities):
                print(f"	Similarity to {job_roles.iloc[j]}: {score:.2f}")

            try:
                plt.figure(figsize=(10, 5))
                bars = plt.bar(job_roles, similarities, color='skyblue')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, 1)
                plt.title(f"Resume {i+1} - Similarity Scores to Job Roles")
                plt.xlabel("Job Role")
                plt.ylabel("Similarity Score")
                for bar, score in zip(bars, similarities):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{score:.2f}", ha='center', va='bottom')
                plt.tight_layout()
                plt.show()
            except Exception as plot_err:
                print(f"Error generating plot for Resume {i+1}: {plot_err}")

    except Exception as e:
        print(f"Error during evaluation: {e}")
