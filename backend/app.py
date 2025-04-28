import os
import re
import json
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import unicodedata
import pandas as pd
import nltk
import inflect
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def remove_non_ascii(words):
    return [unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore') for word in words]

def to_lowercase(words):
    return [word.lower() for word in words]

def remove_punctuation(words):
    return [re.sub(r'[^\w\s]', '', word) for word in words if re.sub(r'[^\w\s]', '', word) != '']

def replace_numbers(words):
    p = inflect.engine()
    return [p.number_to_words(word) if word.isdigit() else word for word in words]

def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words]

def stem_words(words):
    stemmer = LancasterStemmer()
    return [stemmer.stem(word) for word in words]

def lemmatize_verbs(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, pos='v') for word in words]

def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    words = lemmatize_verbs(words)
    return words


def parse_resume(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    
    tokenized_words = word_tokenize(raw_text)
    
    normalized_words = normalize(tokenized_words)
    
    return normalized_words


search_terms = [
    "agile", "ai", "angular", "apache spark", "api testing", "aws",
    "beamer", "binary tree", "binary tree construction", "big data",
    "bitnami wamp & wapp servers", "bootstrap", "c", "c++", "cloud computing",
    "compiler design", "computer graphics", "computer vision", "construct binary tree from string",
    "css", "cyber security", "data science", "data structures & algorithm",
    "deep learning", "devops", "dicom viewer", "discrete mathematics",
    "docker", "dsa", "eclipse ide", "engineering mathematics", "etl",
    "express.js", "fastapi", "figma", "firebase", "flask", "git",
    "github actions", "go", "google colab", "graph theory", "graphql",
    "graphic design", "hadoop", "html", "image processing", "intellij idea",
    "internet of things", "iot", "java", "jenkins", "jest", "jira",
    "jupyter", "jupyter notebook", "keras", "kubernetes", "latex",
    "latex editor", "linux", "machine learning", "mathematical logic",
    "microprocessor based design", "mongodb", "ms office", "mysql",
    "next.js", "nlp", "node.js", "nosql", "notion", "object oriented programming",
    "opencv", "operating system", "oracle", "parsing parenthesis", "php",
    "postman", "power bi", "postgresql", "python", "rdbms", "react",
    "redis", "reinforcement learning", "rest api", "root value", "rust",
    "scala", "scikit-learn", "scrum", "selenium", "set theory", "shell programming",
    "sql", "sql server", "swift", "system design", "tableau", "tailwind css",
    "tensorflow", "theory of computations", "tree from string", "tree parsing",
    "tree traversal", "typescript", "ui/ux design", "unit testing", "vscode",
    "vue.js"
]


blacklist = {
    'developer', 'development', 'technical', 'skills', 'software',
    'web', 'mobile', 'system', 'content', 'management', 'platform',
    'design', 'engineering', 'analysis', 'consultant', 'client', 'needs',
    'assurance', 'technology', 'implementation',
    'knowledge', 'proficiency'
}

search_terms_v2 = [
    "python", "javascript", "html", "css", "react", "node.js", "c++", "java", "sql", "aws", "machine learning", "docker", "kubernetes"
]

def clean_skills(raw_skills):
    skills = re.split(r'[,\n\t\r]+|\s{2,}', raw_skills.strip().lower())
    filtered = [skill.strip() for skill in skills if skill and skill not in blacklist]
    seen = set()
    unique_skills = []
    for skill in filtered:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)
    return ', '.join(unique_skills)


def fetch_jobs_for_cities(cities, pages_to_scrape=3):
    """Fetch jobs for specific cities."""
    base_url = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&postWeek=60&searchType=Home_Search&cboPresFuncArea=35&pDate=Y&sequence=2&startPage='
    
    jobs_data = [] 
    job_counter = 1 

    for city in cities:
        print(f"Fetching jobs for {city}...")

        for page in range(1, pages_to_scrape + 1):
            url = f"{base_url}{page}&txtLocation={city}"
            try:
                response = requests.get(url)
                response.raise_for_status() 
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch page {page} for {city}: {e}")
                continue

            soup = BeautifulSoup(response.text, 'lxml')
            job_list = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

            if not job_list:
                print(f"No jobs found for {city} on page {page}. Moving to next city.")
                break

            for job in job_list:
                posted_tag = job.find('span', class_='sim-posted')
                posted = posted_tag.text.strip() if posted_tag else 'N/A'

                title = job.header.h2.a.text.strip() if job.header and job.header.h2 and job.header.h2.a else 'N/A'
                company_tag = job.find('h3', class_='joblist-comp-name')
                company = company_tag.text.strip() if company_tag else 'N/A'

                skills_div = job.find('div', class_='srp-skills')
                raw_skills = skills_div.text.strip() if skills_div else 'N/A'
                skills = clean_skills(raw_skills)

                link = job.header.h2.a['href'] if job.header and job.header.h2 and job.header.h2.a else 'N/A'

                
                location = 'N/A'
                location_tag = job.find('ul', class_='top-jd-dtl mt-16 clearfix')
                if location_tag:
                    location_li = location_tag.find('li', class_='srp-zindex location-tru')
                    if location_li:
                        if location_li.has_attr('title'):
                            location = location_li['title'].strip()
                        else:
                            location = location_li.text.strip()

                
                job_data = {
                    'Job Number': job_counter,
                    'City': city,
                    'Title': title,
                    'Company': company,
                    'Location': location,
                    'Skills': skills,
                    'Posted': posted,
                    'Link': link
                }
                jobs_data.append(job_data)
                job_counter += 1

    return jobs_data


@app.route('/fetch_jobs', methods=['GET'])
def fetch_jobs():
    cities = ['calicut', 'mumbai', 'bangalore', 'chennai', 'hyderabad', 'kochi', 'trivandrum']
    jobs_data = fetch_jobs_for_cities(cities, pages_to_scrape=3) 
    os.makedirs('javascript_jobs', exist_ok=True)
    with open(os.path.join('javascript_jobs', 'javascript_jobs.json'), 'w', encoding='utf-8') as f:
        json.dump(jobs_data, f, indent=4, ensure_ascii=False)
    
    return jsonify({"success": True, "jobs": jobs_data})


CSV_FILE_PATH = r"C:\Users\aswan\OneDrive\Desktop\project\hexa\backend\jobs_data.csv"


def load_job_data_from_csv():
    job_list = []
    try:
       
        df = pd.read_csv(CSV_FILE_PATH)
        for _, row in df.iterrows():
            job_list.append({
                'Job Number': int(row['Job Number']),
                'Title': row['Title'],
                'Company': row['Company'],
                'Skills': row['Skills'],
                'Link': row['Link']
            })
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return job_list

@app.route('/fetch_job_list', methods=['GET'])
def get_job_list():
   
    page = int(request.args.get('page', 1))  
    jobs_per_page = 10 


    job_list = load_job_data_from_csv()

    # Implement pagination
    start_index = (page - 1) * jobs_per_page
    end_index = start_index + jobs_per_page
    job_page = job_list[start_index:end_index]  # Slice the list for pagination

    return jsonify(job_page)


@app.route('/parse', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files:
        return jsonify({"success": False, "message": "No resume file provided"}), 400

    resume = request.files['resume']
    
    if resume.filename == '':
        return jsonify({"success": False, "message": "Empty file name"}), 400

    # Save the resume temporarily
    filepath = os.path.join(UPLOAD_FOLDER, resume.filename)
    resume.save(filepath)
    print(f"Resume saved at: {filepath}")

    try:
        # Detect and parse PDF or text file
        if filepath.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(filepath)
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                resume_text = file.read()

        # Tokenize and normalize the extracted text
        tokenized_words = word_tokenize(resume_text)
        normalized_words = normalize(tokenized_words)
        normalized_text = ' '.join(normalized_words)

        # Match keywords with the normalized resume text
        found_keywords = [term for term in search_terms_v2 if term.lower() in normalized_text.lower()]
        
        # Get the remaining search terms that were not found in the resume
        unmatched_keywords = [term for term in search_terms_v2 if term.lower() not in [keyword.lower() for keyword in found_keywords]]
        
        # Save found unmatched keywords in a file
        with open("unmatched_keywords.txt", "w", encoding='utf-8') as f:
            for keyword in unmatched_keywords:
                f.write(keyword + "\n")
        
        print(f"Unmatched keywords: {unmatched_keywords}")
        
        return jsonify({
            "success": True,

            "unmatched_keywords": unmatched_keywords
        }), 200

    except Exception as e:
        print("Error parsing resume:", str(e))
        return jsonify({"success": False, "message": "Error parsing resume"}), 500

def clean_skills(raw_skills):
    skills = re.split(r'[,\n\t\r]+|\s{2,}', raw_skills.strip().lower())
    filtered = [skill.strip() for skill in skills if skill and skill not in blacklist]
    seen = set()
    unique_skills = []
    for skill in filtered:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)
    return ', '.join(unique_skills)

@app.route('/web')
def index():
    jobs = fetch_jobs()  # Fetch the jobs data
    return jsonify(jobs)  

# Extract text from PDF
def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text



@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"success": False, "message": "No resume file provided"}), 400

    resume = request.files['resume']
    location = request.form.get('location', '')
    salary = request.form.get('salary', '')
    expected_job = request.form.get('expected_job', '')  # <-- Get expected job title from frontend

    if resume.filename == '':
        return jsonify({"success": False, "message": "Empty file name"}), 400

    filename = secure_filename(resume.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume.save(filepath)

    print(f"Resume saved at: {filepath}")
    print("Location:", location)
    print("Job Expectation (salary):", salary)
    print("Expected Job Title:", expected_job)

    try:
        if filepath.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(filepath)
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                resume_text = file.read()

        final_words = resume_text.split()
        normalized_text = ' '.join(final_words)

        found_keywords = [term for term in search_terms if term.lower() in normalized_text.lower()]
        print("Found Keywords from Resume:", found_keywords)

        jobs_data = fetch_jobs_for_cities([
             'calicut', 'mumbai', 'bangalore', 'chennai', 'hyderabad', 'kochi', 'trivandrum'
        ])

        matching_jobs = []
        seen_job_titles = set()

        for job in jobs_data:
            # Filter by location if provided
            if location and location.lower() not in job['Location'].lower():
                continue
            
            # Filter by expected job title if provided
            if expected_job and expected_job.lower() not in job['Title'].lower():
                continue

            job_skills = [js.lower() for js in job['Skills'].split(', ')]
            match_count = 0
            matched_skills = []

            for keyword in found_keywords:
                if keyword.lower() in job_skills:
                    match_count += 1
                    matched_skills.append(keyword)

            if match_count >= 2:
                job_copy = job.copy()
                job_copy["match_count"] = match_count
                job_copy["matched_skills"] = matched_skills

                if job_copy["Title"].lower() not in seen_job_titles:
                    matching_jobs.append(job_copy)
                    seen_job_titles.add(job_copy["Title"].lower())

        matching_jobs.sort(key=lambda x: x["match_count"], reverse=True)

        return jsonify({
            "success": True,
            "matching_jobs": matching_jobs
        }), 200

    except Exception as e:
        print(f"Error during resume processing: {e}")
        return jsonify({"success": False, "message": "Error processing resume."}), 500

if __name__ == '__main__':
    app.run(debug=True)
