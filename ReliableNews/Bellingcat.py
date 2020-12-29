#!/usr/bin/env python
# coding: utf-8

# # Scrape news articles from https://www.bellingcat.com/
# This script uses Python library, BeautifulSoup, for scraping. The infromation requested is: title, published date and text. All data are stored in Mongodb. Additional data which are stored in the database are: id for each article and source of article.
# Pymongo is the official MongoDB API that allows to easily perform mongodb operations with Python.

# In[1]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import RReadWriteCSV


# In[2]:


url = 'https://www.bellingcat.com/category/news/' # url to scrape from
hrefs=['africa/','americas','mena','rest-of-world','uk-and-europe']
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser') # give a BeautifulSoup object, which represents the document 
                                                  # as a nested data structure
count=0 #count scraped pages


# In[ ]:


def scraping(array_of_ids):
    for adds in hrefs:
        page = requests.get(url+adds) # to get a webpage
        soup = BeautifulSoup(page.content, 'html.parser')  # give a BeautifulSoup object, which represents the document 
                                                           # as a nested data structure

        div=soup.find_all("h2") # class of required divs
        for b in div: # selected div from part of the page containing the article link
            a = b.find('a', href=True)  # all <a href> links 
            if a is not None:
                article=requests.get(a['href'])
                soup = BeautifulSoup(article.content, 'html.parser')
                #test=soup.find(class_="CardHeadline").find("h2") # link testing

                news = {} # structure for scraped data
                news['_id']=a['href']
                
                if news['_id'] in array_of_ids:
                    continue # ako pravi problem prvo ovo proveri     
                array_of_ids.append(news['_id'])
                try:
                    news['source']=a['href']
                    news['title'] = b.get_text()

                    pom = soup.find("p", {"class":["meta","time"]}).get_text()
                    news['date']=datetime.strptime(pom, '\n\t\t\t\t\t%B %d, %Y\t\t\t\t')
                    print(news['date'])

                    #the text is composed of several smaller ones 
                    array_text=soup.find("section", itemprop="articleBody").find_all("p")
                    text=''

                    for t in array_text:
                        text+=t.get_text()

                    news['text']= text
                    RReadWriteCSV.write(news)
                except:
                    continue


# In[ ]:




