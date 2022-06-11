# Import Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Add Questions that need user input
# What is the job title?
# What is the job location?
# set the variable "position" to the user input
position = input("What position are you looking for? ")
# set the variable "location" to the user input
location = input("What location do you want to search? ")

# define a method to get data from website
# "extract" method will format the website, extract data, and store it in a "soup" object
def extract(position, location_, page):
    # headers is a dictionary that contains the headers of the request to the website
    # header allows for webserver authentication 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    # url is the website that we want to scrape
    # use f string to format position and location based on user input
    url = f'https://www.indeed.com/jobs?q={position}&l={location_}&start={page}'
    # set the variable "r" equal to get method using variables "url" and "headers" as arguments
    r = requests.get(url, headers)
    # set the variable "soup" equal to BeautifulSoup method using variable "r" with content method, and html with parser method as an arguments
    soup = BeautifulSoup(r.content, 'html.parser')
    # return the variable "soup"
    return soup

# define a method to parse the soup object
# this method transforms data from "soup" object
def transform(soup):
    # create variable "div" set it equal to:
        # find all divs with class "jobsearch-SerpJobCard" 
    divs = soup.find_all('div', class_='job_seen_beacon')
    # for loop to iterate through each div in "divs"
    for item in divs:
        # create variable "title" set it equal to:
            # find all h2 tags with class "job_seen_beacon"
        title = item.find('h2').text.strip('new')
          
        try: 
            # set the variable location to:
            #   look for all divs with a class of companyLocation
            location = item.find('div', class_='companyLocation').text.strip()
        except:
            location = ''
        # set the variable company equal to:
        #   find all span tags with a class of companyName
        company = item.find('span', class_='companyName').text.strip()
        try:
            # set the variable salary equal to:
            #   find all div tags with a class of attribute_snippet  
            salary = item.find('div', class_='attribute_snippet').text.strip()
        except:
            salary = ''
        # set the variable summary equal to:
        #  find all div tags with a class of 'job-snippet'        
        summary = item.find('div', class_='job-snippet').text.strip().replace('\n', '')
        # need a url to each job
        # define a dictionary named "job" and use names of variables as keys  
        job = {
            'title' : title,
            'location' : location,
            'company' : company,
            'salary' : salary,
            'summary' : summary
        }
        # append the dictionary "job" to the joblist that will be created below
        joblist.append(job)
    return

# run the actual program to store parsed data in a dataframe
# create a list named "joblist"
joblist = []
# create a for loop to iterate through the pages of the website
for i in range(0, 40, 10):
    print(f'Getting page, {i}')
    # set variable "c" equal to:
        # call the method "extract" with variables "position" and "location" and "30 pages" as arguments
    c = extract(position, location, 30)
    # call the method transform and use "c" as an argument
    transform(c)

# create a dataframe named "df" with the argument joblist
df = pd.DataFrame(joblist)
print(df.head())
# save the dataframe to a csv file named jobs
df.to_csv('jobs.csv')