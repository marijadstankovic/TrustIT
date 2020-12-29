#!/usr/bin/env python
# coding: utf-8

# # The script for scraping news from aljazeera.com

# The libraries included are for scraping (requests and BeautifulSoup) and interacting with mongo database

# In[5]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import RReadWriteCSV ################################################


# Pages where news can be found are:

# In[6]:


start_pages=["https://www.aljazeera.com/news/", "https://www.aljazeera.com/topics/regions/middleeast.html", 
       "https://www.aljazeera.com/topics/regions/africa.html", "https://www.aljazeera.com/topics/regions/asia-pacific.html",
       "https://www.aljazeera.com/topics/regions/us-canada.html", "https://www.aljazeera.com/topics/regions/latin-america.html", 
      "https://www.aljazeera.com/topics/regions/europe.html", "https://www.aljazeera.com/topics/regions/asia-pacific.html"]


# The variable i counts how many successful writings we have.
# Links are taken from each page

# Each link is being checked:
#     if the href starts with "/progremmes" that page cannot be scraped with the link
#     if the link is already in the base it won't be added
# Additionaly in case some exception occur try-except block will handle it: it won't affect the next news to be scraped

# In[7]:


def scraping(array_of_ids):
    for start_page in start_pages:
        page = requests.get(start_page)
        supa = BeautifulSoup(page.content, 'html.parser')
        body = supa.find(id = "placeholder1")
        linkovi = body.find_all("div", class_="col-sm-7 topics-sec-item-cont")
        for link in linkovi:
            try:
                news = {}
                href=link.find_all('a')[1].get('href')
                if href in array_of_ids:##############################
                    continue # ako pravi problem prvo ovo proveri
                    
                array_of_ids.append(href)   ###############################
                if href[0:11] != "/programmes":
                    #check if the news is already in the db
                    newLink = 'https://www.aljazeera.com' + href    
                    page = requests.get(newLink)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    
                    news['_id'] = href
                    news['title'] = soup.find(class_="article-heading").find("h1").get_text() 
                    news['date'] = soup.find(class_="timeagofunction")['datetime']                
                    news['source'] = "https://www.aljazeera.com"

                    div = soup.find(class_="article-p-wrapper")
                    p_text=div.find_all('p')
                    news['text']=''

                    for x in p_text:
                        news['text'] += x.get_text()
                    RReadWriteCSV.write(news)##################################
                         
            except: 
                continue
            


# Finally, the result of scaping is printed

# In[8]:


test=[]
scraping(test)
print(test)
print("nista onda")

