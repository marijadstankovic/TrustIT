#!/usr/bin/env python
# coding: utf-8

# # Script for scraping news from bbc.com

# The first cell scrapes only one news from this site (ex. "https://www.bbc.com/news/world-europe-50266955") and prints it. The date on the web page is represented in unusual format so some extra string manipulations are used.

# In[1]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import RReadWriteCSV

page = requests.get("https://www.bbc.com/news/world-europe-50266955")
soup = BeautifulSoup(page.content, 'html.parser')

news={}
news['title'] = soup.find("h1").get_text()
news['date'] = soup.find(class_="date date--v2")['data-datetime']
parts = news['date'].split(" ")
if len(parts[0])<2:
    parts[0]="0"+parts[0]
news['date'] = parts[0]+" "+parts[1]+" "+parts[2]
news['date'] = datetime.strptime(news['date'], "%d %B %Y")

news['source'] = "https://www.bbc.com"
news['_id'] = "/news/world-europe-50266955"
news['text'] = ''

p_s = soup.find(class_="story-body").find_all('p')
for p in p_s:
    news['text'] = news['text'] + p.get_text()
print(news)


# Next cell represenst connecting to the base, searching for important links on the main page, discarding sports news, checking if the link is for news(it is noticed that links for news end with numbers, while links for other pages don't). The last check is to see if the news is already in the database. The rest of the code is like the one before

# In[2]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import RReadWriteCSV

page = requests.get("https://www.bbc.com/news/world")
soup = BeautifulSoup(page.content, 'html.parser')
div = soup.find(class_="gel-layout gel-layout--equal").find_all("a")

def scraping(array_of_ids):
    for a in div:
        try:
            if a['href'][0:6] == '/sport':
                continue
            if a['href'][-1:]<='9' and a['href'][-1:]>='0':

                myLink="https://www.bbc.com"+a['href']
                news_page = requests.get(myLink)
                news_soup = BeautifulSoup(news_page.content, 'html.parser')

                news={}
                news['_id'] = a['href']
                
                if news['_id'] in array_of_ids:
                    continue # ako pravi problem prvo ovo proveri     
                array_of_ids.append(news['_id'])
                
                news['title'] = news_soup.find("h1").get_text()

                news['date'] = news_soup.find(class_="date date--v2")['data-datetime']
                parts = news['date'].split(" ")
                if len(parts[0])<2:
                    parts[0]="0"+parts[0]
                news['date'] = parts[0]+" "+parts[1]+" "+parts[2]
                news['date'] = datetime.strptime(news['date'], "%d %B %Y")      
                news['source'] = "https://www.bbc.com"
                news['text'] = ''

                p_s = news_soup.find(class_="story-body__inner").find_all('p')
                for p in p_s:
                    print(p.get_text())
                    news['text'] += p.get_text()
                RReadWriteCSV.write(news)
        except:
            continue

    print("end")


# When the scraping is finished, end is printed.
