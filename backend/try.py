import requests
from bs4 import BeautifulSoup
import csv
import time

def clean_skills(raw_skills):
    """Clean and return the list of skills as a comma-separated string."""
    return ', '.join(skill.strip() for skill in raw_skills.split(','))

def fetch_jobs_for_cities(cities, pages_to_scrape=5):
    """Fetch jobs for specific cities."""
    base_url = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&postWeek=60&searchType=Home_Search&cboPresFuncArea=35&pDate=Y&sequence=2&startPage='
    
    jobs_data = []  # Store all jobs data
    job_counter = 1  # For unique job numbering

    for city in cities:
        print(f"Fetching jobs for {city}...")

        for page in range(1, pages_to_scrape + 1):
            url = f"{base_url}{page}&txtLocation={city}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check if the request was successful
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

                # Extract location
                location = 'N/A'
                location_tag = job.find('ul', class_='top-jd-dtl mt-16 clearfix')
                if location_tag:
                    location_li = location_tag.find('li', class_='srp-zindex location-tru')
                    if location_li:
                        if location_li.has_attr('title'):
                            location = location_li['title'].strip()
                        else:
                            location = location_li.text.strip()

                # Store job data
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

            time.sleep(1)  # Be polite to the server by pausing between requests

    return jobs_data

def save_jobs_to_file(jobs_data, filename='jobs_data.csv'):
    """Save fetched jobs data to a CSV file."""
    if not jobs_data:
        print("❌ No jobs data to save.")
        return

    keys = jobs_data[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs_data)
    print(f"✅ Jobs saved to '{filename}' successfully.")

def print_jobs(jobs_data):
    """Print job details to console."""
    for job in jobs_data:
        print(f"Job Number: {job['Job Number']}")
        print(f"City: {job['City']}")
        print(f"Title: {job['Title']}")
        print(f"Company: {job['Company']}")
        print(f"Location: {job['Location']}")
        print(f"Skills: {job['Skills']}")
        print(f"Posted: {job['Posted']}")
        print(f"Link: {job['Link']}")
        print('-' * 60)

# Main run
if __name__ == "__main__":
    cities = ['new delhi','calicut','thrissur','mumbai','bangalore','kolkata','chennai','hyderabad','pune','kochi','noida','trivandrum']
  # Cities in Kerala
    jobs = fetch_jobs_for_cities(cities, pages_to_scrape=5)  # ⬅️ Scrape 5 pages (around 125 jobs!)
    if jobs:
        print_jobs(jobs)  # Print the job details
        save_jobs_to_file(jobs)  # Save the job data to a CSV file
    else:
        print("No jobs fetched.")
