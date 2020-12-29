#!/usr/bin/env python
# coding: utf-8

# # Scrape news articles from www.theatlantic.com
# 
# 
#    This script uses Python library, BeautifulSoup, for scraping.
# The infromation requested is: title, published date and text.
# All data are stored in Mongodb. Additional data which are stored in the database are: id for each article and source of article.<br>

# In[4]:


import requests
from bs4 import BeautifulSoup
import RReadWriteCSV


# In[5]:


url = 'https://www.theatlantic.com/latest'
url_ = 'https://www.theatlantic.com'# url to scrape from


# In[6]:


def scraping(array_of_ids):
    count=0
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') # give a BeautifulSoup object, which represents the document 
                                                      # as a nested data structure
    div=soup.find_all(class_="article blog-article")
    for b in div: # selected div from part of the page containing the article link
        a = b.find('a', href=True)  # all <a href> links 
        if a is not None:
            try:
                article=requests.get(url_+a['href'])
                soup = BeautifulSoup(article.content, 'html.parser')
                test=soup.find("h1",class_="c-article-header__hed")
                if test is not None: # if the link is good test is not None
                    news = {} # structure for scraped data
                    news['_id']=a['href']
                    if news['_id'] in array_of_ids:
                        continue    
                    array_of_ids.append(news['_id'])

                    news['source']=url_ + a['href']
                    news['title'] = test.get_text()
                    # date format of the article is: 1 NOVEMBER 2019
                    date= soup.find("time", {"class":["c-dateline","c-dateline--ideas"]})['datetime'].split("T")
                    news['date'] =date[0]

                    #the text is cmposed of several smaller ones 
                    array_text=soup.find("section", {"class":["l-article__section","s-cms-content"]}).find_all("p")
                    text=''

                    for t in array_text:
                        text+=t.get_text() 

                    news['text']= text
                    count+=1
                    RReadWriteCSV.write(news)
            except:
                continue
    print(str(count) + "scrabed articles")

