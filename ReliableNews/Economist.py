#!/usr/bin/env python
# coding: utf-8

# # Scrape news articles from www.economist.com
# This script uses Python library, BeautifulSoup, for scraping. The infromation requested is: title, published date and text. All data are stored in Mongodb. Additional data which are stored in the database are: id for each article and source of article.
# 
# Pymongo is the official MongoDB API that allows to easily perform mongodb operations with Python.

# In[4]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import RReadWriteCSV


# The list _hrefs_ contains name of topics on this site. <br>
# The link to the every topic is made like: **url + topic_name** <br>
# _topic_name_ is the element from a list.

# In[5]:


url = 'https://www.economist.com' # url to scrape from
hrefs=['/latest/', '/leaders/', '/briefing/','/united-states/', '/the-americas/', '/asia/', '/china/','/middle-east-and-africa/','/europe/', '/britain/']


# The first for statement iterates through a list of topics on this site. <br>
# The second for statement iterates through array of divs with the same class - these divs hold a link to news that is going to be scraped. <br>
# _this array of divs are located on the link: url + topic_name_

# In[6]:

def scraping(array_of_ids):
    for adds in hrefs: # first for statement
        page = requests.get(url+adds) # to get a webpage
        soup = BeautifulSoup(page.content, 'html.parser')  # give a BeautifulSoup object, which represents the document 
                                                           # as a nested data structure

        div=soup.find_all(class_="teaser") # class of required divs
        for b in div: # second for statement
            a = b.find('a', href=True)  # all <a href> links 
            if a is not None:
                try:
                    # checking if the article already exists in the database
                    news = {} # structure for scraped data
                    news["_id"]=a['href']

                    if news["_id"] in array_of_ids:
                        continue # ako pravi problem prvo ovo proveri     
                    array_of_ids.append(news["_id"])
                     
                    article=requests.get(url+a['href'])
                    soup = BeautifulSoup(article.content, 'html.parser')
                    test=soup.find(class_="article__headline") # link testing
                    if test is not None: # if the link is good test is not None
                        news["source"]=url
                        news['title'] = soup.find(class_="article__headline").get_text()

                        for i in soup.findAll('time'):
                            if i.has_attr('datetime'):
                                news['date']=i['datetime']


                        #the text is composed of several smaller ones 
                        array_text=soup.find_all(class_="article__body-text")
                        news['text']=''
                        for t in array_text:
                            news['text']+=t.get_text()
                        RReadWriteCSV.write(news)
                except:
                    continue
                    #writing data into database

