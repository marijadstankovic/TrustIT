#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import logging
import ReadWriteCSV

def scraping(array_of_ids):
    url = 'https://newrepublic.com' # url to scrape from
    hrefs=['/latest/', '/tags/politics/', '/tags/culture/', '/tags/climate-change/']
    
    total=0
    successfull=0    
    for adds in hrefs:
        page = requests.get(url+adds)  # to get a webpage
        soup = BeautifulSoup(page.content, 'html.parser') # give a BeautifulSoup object, which represents the document 
                                                   # as a nested data structure
        div=soup.find_all(itemprop="headline") # itemprop of required divs
        for b in div: # selected div from part of the page containing the article link
            a = b.find('a', href=True)  # all <a href> links 
            if a is not None:
                total=total+1
                
                
                if a['href'] in array_of_ids:  # checking if the article already exists in the database
                    continue
                array_of_ids.append(a['href'])
                
                article=requests.get(url+a['href'])
                soup = BeautifulSoup(article.content, 'html.parser')
                test=soup.find(class_="article-headline") # link testing
                if test is not None:  # if the link is good test is not None
                    #news['_id']=a['href']
                    news={}
                    news['_id'] = a['href']
                    news['source']=url
                    news['title'] = soup.find(class_="article-headline").get_text()

                    var=soup.find(class_="article-date").get_text()
                    news['date']=datetime.strptime(var, '%B %d, %Y')
#                     print(news['date'])
                    #the text is composed of several smaller ones 
                    array_text=soup.find("div","article-body").find_all("p")
                    text=''
                    
                    for t in array_text:
                        text+=t.get_text()

                    news['text']= text
                    
                    #writing data into database
                    print(news["_id"])
                    ReadWriteCSV.write(news)
                    
                    successfull=successfull+1
                    
    print(successfull)
    print(total)


# In[ ]:


# scraping(ReadWriteCSV.read())

