from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import re
import numpy as np

def build_training_data(job_skills_list):
    """
    Converts the job skills list into a 2D array of job vectors for use in cosine similarity calculations.
    Each job vector is a binary representation of the skills present in the job description.

    Args:
        job_skills_list (list): A list of job descriptions, where each description is a string of skills.

    Returns:
    job_vectors: A 2D numpy array where each row corresponds to a job and each column corresponds to a skill.
    all_skills: A list of all unique skills extracted from the job descriptions.
    """

    try:
        if not job_skills_list:
            print("Warning: job_skills_list is empty.")
            return np.array([]), []
            

        all_skills = list(set(' '.join(job_skills_list).lower().split()))  # This will give us a list of all the unique (non-duplicate) skills in the job descriptions, and we will use this to vectorize the candidate skills


        job_vectors = []  # this will be the array that will store all the job vectors in a 2D format later 

        for job in job_skills_list:   # each index in job corresponds to the entire skill set for that job, since the list returned from job_skills = jobs_df['skills'].tolist() looks like 
                                      # "Python Data Analysis Excel SQL",                      index 0 → Data Analyst
                                      # "Python Machine Learning Deep Learning Statistics",    index 1 → ML Engineer
                                      # "Java C++ Python Git"                                  index 2 → Software Dev        

            job_vector = []  # each job will have a unique array 
            job_words = job.lower().split()  # This turns the job into a list of words, so that we can check if the skill is in the job description

            for skill in all_skills:
                if skill in job_words:
                    job_vector.append(1)  # if the skill is in the job description, append 1 to the job_vector
                else:
                    job_vector.append(0)  # if the skill is not in the job description, append 0 to the job_vector
                                          # The reason we added 1s and 0s is because we are going to use cosine similarity to compare the job vectors, and we need a numerical representation of the skills in the job description

            job_vectors.append(job_vector)  # each job vector is appended to the job_vectors list, which will be a 2D array

        job_vectors = np.array(job_vectors)  # convert the job_vectors list to a numpy array so that we can use cosine similarity on it

        return job_vectors, all_skills  # job_vectors is a 2D array where each row corresponds to a job and each column corresponds to a skill, and all_skills is a list of all the skills in the job descriptions which will be used to vectorize the candidate skills 
    
    except Exception as e:
        print(f"Error building trainingdata:{e}")

def vectorize_candidate(candidate_skills, all_skills): 
    """
    Converts the candidate skills into a 1D array for use in cosine similarity calculations.
    Each candidate skill is represented as a binary value indicating its presence in the all_skills list.

    Args:
        candidate_skills (list): A list of skills extracted from the candidate's resume.
        all_skills (list): A list of all unique skills extracted from the job descriptions.
    
    Returns:
        job_vector: A 1D numpy array where each element corresponds to a skill in the all_skills list.
    """

    try: 

        job_vector=[] #this will be the array that will store the candidate skills in a 1D format later 

        for skill in all_skills: #for each skill in the all_skills list, we will check if it is in the candidate skills list
                                 #what makes this function different from the build_training_data function is that we are not checking if the skill is in the job description, but if it is in the candidate skills list
                                 #However they will both be the same length, since we are using the same all_skills list to vectorize the skills in the job description and the candidate skills
            if skill in candidate_skills:
                job_vector.append(1) #if the skill is in the candidate skills list, append 1 to the job_vector
            else:
                job_vector.append(0) #if the skill is not in the candidate skills list, append 0 to the job_vector

        return np.array([job_vector]) #convert the job_vector list to a numpy array so that we can use cosine similarity on it

    except Exception as e:
        print(f"Error vectorizing candidate skills: {e}")
        
def evaluate_resumes(resume_files, job_skills_list, extract_text_func, extract_skills_func, job_roles):
    """
    This function processes each resume, extracts the candidate's skills, and compares them to the job descriptions using cosine similarity.
    It also generates a bar plot to visualize the similarity scores for each job role.

    Args:
        resume_files (list): A list of file paths to the resumes to be evaluated.
        job_skills_list (list): A list of job descriptions, where each description is a string of skills.
        extract_text_func (function): A function to extract text from the resume files.
        extract_skills_func (function): A function to extract skills from the resume text.
        job_roles (pd.Series): A pandas Series containing the job roles corresponding to the job descriptions.

    Returns:
        None: The function prints the results and generates plots for each resume.
    """
    try:
        job_vectors, all_skills = build_training_data(job_skills_list) #build the training data using the job skills list, and also extracting the all_skills list from it to use it on other functions 
        
        # Safety check for empty skills
        if len(all_skills) == 0:
            print("Warning: No skills were extracted.")
            return

        for i, resume_path in enumerate(resume_files): #this will iterate through the resume files and give us the index of the resume file as well as the path to the resume file
            print("\n---------------------------")

            text = extract_text_func(resume_path) #extract the entire resume file into a string 
            if not text:
                print(f"Warning: No text extracted from {resume_path}.")
                continue

            name_matches = re.findall(r'Name[:\s]*([A-Z][a-z]+\s[A-Z][a-z]+)', text) #this will find the name of the candidate from the resume's text by using the regex module
            if name_matches:
                name = name_matches[0] #this just ensures that we are only getting the first name in case there are multiple names in the resume, because each name that the regex module finds will be stored in a seperate index for it like name_matches = ["Khaled Almalki", "Yazan Alghamdi", ...]
            else:
                name = "Name not found"

            email_matches = re.findall(r'[\w.-]+@[\w.-]+', text) #this will find the email of the candidate from the resume's text by using the regex module
            if email_matches:
                email = email_matches[0] #this just ensures that we are only getting the first email in case there are multiple emails in the resume, because each email that the regex module finds will be stored in a seperate index for it like email_matches = ["khaledAlmalki@uj.edu.sa", "yazanAlghamdi@uj.edu.sa", ...]
            else:
                email = "Email not found"

            print(f"Processing Resume {i+1} | name :  {name} | email :  ({email})") #this will print the name and email of the candidate in a readable format

            skills = extract_skills_func(text, job_skills_list) #this will extract the skills from the resume's text using the extract_skills_func function, and also passing the job_skills_list to it so that we can check if the skills are in the job description or not
                                                                #the skills extracted from this function will be used to vectorize the candidate skills using the vectorize_candidate function
                                                                #it will only return the skills that match the job description, and not all the skills in the resume
            if not skills:
                print(f"Warning: No skills matched from resume {i+1}.")
                continue

            print("Extracted Candidate Skills:", skills) #this will print the skills that were extracted from the resume in a readable format

            candidate_vector = vectorize_candidate(skills, all_skills) #this will vectorize the candidate's skills and return it in a 1D format that consists of 1s and 0s
            

            similarities = cosine_similarity(candidate_vector, job_vectors)[0] #cosine similarity will return a 2D array with only 1 row, so we use the [0] to get the first row of the array, which will be a 1D array that contains the similarity scores between the candidate's skills and the job descriptions
                                                                               #The candidate vector is a 1D array, and the job vectors is a 2D array, both of the same length, so we can use cosine similarity to compare them
                                                                               #each row from the job_vectors array will be compared to the candidate vector, and the similarity score of each job will be added into 

            max_score = max(similarities) #this will give us the maximum score from the similarities array, which will be used to find the index of the job that is most similar to the candidate's skills

            predicted_indices = [] #this will be used to store the indices of the jobs that have the maximum score, in case there are multiple jobs with the same score
            for j, similarity_score in enumerate(similarities): #this will iterate through the similarities array and give us the index of the job as well as the similarity score of the job
                if similarity_score == max_score:
                    predicted_indices.append(j) #this will append the index of the job to the predicted_indices list if the similarity score is equal to the maximum score
            predicted_idx = predicted_indices[0] #this will give us the index of the job that is most similar to the candidate's skills, and we will use this to get the job role from the job_roles list using the iloc panda function
                                                 #we used [0] to get the first index of the predicted_indices list, since it is possible that there are multiple jobs with the same score, and we only want to get the first one

            print(f"{name} ({email}) most suits the role: {job_roles.iloc[predicted_idx]}") #this will print the name and email of the candidate, and the job role that is most similar to the candidate's skills in a readable format
            for j, similarity_score in enumerate(similarities): #this will iterate through the similarities array and give us the index of the job as well as the similarity score of the job
                print(f"	Similarity to {job_roles.iloc[j]}: {similarity_score:.2f}")

            try:
                plt.figure(figsize=(10, 5)) # Set the figure size for better visibility
                bars = plt.bar(job_roles, similarities, color='skyblue') # Create a bar plot for the similarities
                plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
                plt.ylim(0,1) # Set y-axis limit to 0-1 for similarity scores
                plt.title(f"Resume {i+1} - Similarity Scores to Job Roles") # Set the title of the plot
                plt.xlabel("Job Role") # Set x-axis label
                plt.ylabel("Similarity Score") # Set y-axis label
                for bar, similarity_score in zip(bars, similarities): # Annotate each bar with its similarity score 
                                                                      #we used zip to iterate both lists at the same time since they have the same length, and we can use the index of the bar to get the similarity score from the similarities array
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{similarity_score:.2f}", ha='center') # Add the similarity score above each bar 
                plt.tight_layout() # Adjust layout to prevent clipping of tick-labels
                plt.show() # print the plot to the screen
            
            except Exception as plot_err:
                print(f"Error generating plot for Resume {i+1}: {plot_err}")

    except Exception as e:
        print(f"Error during evaluation: {e}")
