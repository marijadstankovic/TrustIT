#!/usr/bin/env python
# coding: utf-8

# # Scrape news articles from www.snopes.com
# 
# 
#    This script uses Python library, BeautifulSoup, for scraping.
# The infromation requested is: title, published date and text.
# All data are stored in Mongodb. Additional data which are stored in the database are: id for each article and source of article.<br>
# Pymongo is the official MongoDB API that allows to easily perform mongodb operations with Python.

# In[1]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import RReadWriteCSV


# In[2]:


url = 'https://www.snopes.com/news/' # url to scrape from


# The for statement iterates through array of divs with the same class - these divs hold a link to news that is going to be scraped.

# In[3]:


def scraping(array_of_ids):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') # give a BeautifulSoup object, which represents the document 
                                                      # as a nested data structure

    div=soup.find_all(class_="media-wrapper") # class of required divs
    for b in div: # selected div from part of the page containing the article link
        a = b.find('a', href=True)  # all <a href> links 

        if a is not None:
            article=requests.get(a['href'])
            soup = BeautifulSoup(article.content, 'html.parser')
            test=soup.find(class_="post-header").find("h1") # link testing
            if test is not None: # if the link is good test is not None
                news = {} # structure for scraped data
                news['_id']=a['href']
                
                if news['_id'] in array_of_ids:
                    continue      
                array_of_ids.append(news['_id'])
                
                news['source']=url
                news['title'] = soup.find(class_='post-header').find("h1").get_text()

                # date format of the article is: 1 NOVEMBER 2019
                var=soup.find(class_="date-published").get_text()
                news['date']=datetime.strptime(var, '%d %B %Y')

                #the text is cmposed of several smaller ones 
                array_text=soup.find("div", "content").find_all("p")
                news['text']=''

                for t in array_text:
                    news['text']+=t.get_text()
                RReadWriteCSV.write(news)


# In[ ]:




