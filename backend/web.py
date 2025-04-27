import requests
from bs4 import BeautifulSoup
import re

# Words to remove
blacklist = {
    'developer', 'development', 'technical', 'skills', 'software',
    'web', 'mobile', 'system', 'content', 'management', 'platform',
    'design', 'engineering', 'analysis', 'consultant', 'client', 'needs',
    'assurance', 'technology', 'implementation', 'problem', 'solving',
    'knowledge', 'proficiency'
}

def clean_skills(raw_skills):
    # Normalize and split by non-word characters or excessive whitespace
    skills = re.split(r'[,\n\t\r]+|\s{2,}', raw_skills.strip().lower())
    
    # Remove blacklist words and strip each skill
    filtered = [skill.strip() for skill in skills if skill and skill not in blacklist]

    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in filtered:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)

    return ', '.join(unique_skills)

def fetch_jobs():
    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=javascript&txtLocation='
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    job_list = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    with open('javascript_jobs.txt', 'w', encoding='utf-8') as file:
        file.write("[\n")  # Start of the list

        for index, job in enumerate(job_list, 1):
            posted_tag = job.find('span', class_='sim-posted')
            posted = posted_tag.text.strip() if posted_tag else 'N/A'

            if 'few' in posted.lower():
                title = job.header.h2.a.text.strip() if job.header and job.header.h2 and job.header.h2.a else 'N/A'
                company_tag = job.find('h3', class_='joblist-comp-name')
                company = company_tag.text.strip() if company_tag else 'N/A'

                skills_div = job.find('div', class_='srp-skills')
                if skills_div:
                    raw_skills = skills_div.text.strip()
                    skills = clean_skills(raw_skills)
                else:
                    skills = 'N/A'

                link = job.header.h2.a['href'] if job.header and job.header.h2 and job.header.h2.a else 'N/A'

                file.write("  {\n")
                file.write(f"    'Job Number': {index},\n")
                file.write(f"    'Title': '{title}',\n")
                file.write(f"    'Company': '{company}',\n")
                file.write(f"    'Skills': '{skills}',\n")
                file.write(f"    'Link': '{link}'\n")
                file.write("  },\n")

        file.write("]\n")  # End of the list

fetch_jobs()
