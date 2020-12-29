#!/usr/bin/env python
# coding: utf-8

# # Scrape news articles from https://apnews.com/
# 
# 
#    This script uses Python library, BeautifulSoup, for scraping.
# The infromation requested is: title, published date and text.
# All data are stored in Mongodb. Additional data which are stored in the database are: id for each article and source of article.<br>
# Pymongo is the official MongoDB API that allows to easily perform mongodb operations with Python.

# In[ ]:


import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import RReadWriteCSV


# The list hrefs contains name of topics on this site. <br>
# The link to the every topic is made like: url + topic_name
# topic_name is the element from a list.

# In[ ]:


today = date.today()
url = 'https://apnews.com' # url to scrape from
hrefs=['/apf-topnews/','/apf-oddities/','/apf-technology/','/apf-business/','/apf-usnews/','/apf-science/','/apf-intlnews/','/apf-politics/','/apf-religion/']


# The first for statement iterates through a list of topics on this site. <br>
# The second for statement iterates through array of divs with the same class - these divs hold a link to news that is going to be scraped. <br>
# _this array of divs are located on the link: url + topic_name_

# In[ ]:


def scraping(array_of_ids):
    successful=0
    for adds in hrefs:
        page = requests.get(url+adds) # to get a webpage
        soup = BeautifulSoup(page.content, 'html.parser')  # give a BeautifulSoup object, which represents the document 
                                                           # as a nested data structure

        div=soup.find_all(class_="CardHeadline") # class of required divs

        for b in div: # selected div from part of the page containing the article link
            a = b.find('a', href=True)  # all <a href> links 
            if a is not None:
                # checking if the article already exists in the database
                
                news = {} # structure for scraped data
                news['_id']=a['href']
                    
                if news['_id'] in array_of_ids:
                    continue    
                array_of_ids.append(news['_id'])
                try:
                    article=requests.get(url+a['href'])
                    soup = BeautifulSoup(article.content, 'html.parser')
                    test=soup.find(class_="CardHeadline").find("h1") # link testing
                    if test is not None:  # if the link is good test is not None
                        news['source']=url
                        news['title'] = soup.find(class_='CardHeadline').find("h1").get_text()

                        var=soup.find(class_="Timestamp").get_text()
                        news['date']=datetime.strptime(var, '%B %d, %Y %Z')

                        #the text is composed of several smaller ones 
                        array_text=soup.find("div", "Article").find_all("p")
                        text=''

                        for t in array_text:
                            text+=t.get_text()
                        news['text']= text
                        successful=successful+1
                        RReadWriteCSV.write(news)
                except:
                    continue
            print(successful)



# In[ ]:


test=[]
scraping(test)

