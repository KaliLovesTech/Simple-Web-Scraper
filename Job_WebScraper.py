# Import Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Add Questions that need user input
# What is the job title?
# What is the job location?
position = input("What position are you looking for? ")
location = input("What location do you want to search? ")

# defines method to format website, extract data, and store it in a "soup" object
def extract(position, location_, page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q={position}&l={location_}&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup