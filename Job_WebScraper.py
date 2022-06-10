# Import Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Add Questions that need user input
# What is the job title?
# What is the job location?
position = input("What position are you looking for? ")
location = input("What location do you want to search? ")

# define a method to get data from website
# "extract" method will format the website, extract data, and store it in a "soup" object
def extract(position, location_, page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q={position}&l={location_}&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# define a method to parse the soup object
# this method transforms data from "soup" object
def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title = item.find('h2').text.strip('new')
        try: 
            location = item.find('div', class_='companyLocation').text.strip()
        except:
            location = ''
        company = item.find('span', class_='companyName').text.strip()
        try:
            salary = item.find('div', class_='attribute_snippet').text.strip()
        except:
            salary = ''
        summary = item.find('div', class_='job-snippet').text.strip().replace('\n', '')
        # need a url to each job

        job = {
            'title' : title,
            'location' : location,
            'company' : company,
            'salary' : salary,
            'summary' : summary
        }
        joblist.append(job)
    return

# run the actual program to store parsed data in a dataframe
joblist = []
for i in range(0, 40, 10):
    print(f'Getting page, {i}')
    c = extract(position, location, 30)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')