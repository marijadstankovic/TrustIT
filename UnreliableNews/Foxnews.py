#!/usr/bin/env python
# coding: utf-8

# In[5]:

from IPython.core.debugger import set_trace
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import traceback
import logging
import ReadWriteCSV

def scraping(array_of_ids):
    
    url = 'https://www.foxnews.com' # url to scrape from
    hrefs=['/us/', '/world/', '/opinion/', '/politics/', '/entertainment/', '/business/']
    i=0
    total = 0
    successfull = 0    
    for adds in hrefs:  # first for statement
        page = requests.get(url+adds) # to get a webpage
        soup = BeautifulSoup(page.content, 'html.parser') # give a BeautifulSoup object, which represents the document 
                                                           # as a nested data structure
        div=soup.find_all(class_="title")  # class of required divs

        for b in div:  # second for statement
            
            a = b.find('a', href=True)  # all <a href> links 
            if a is not None:
                if a['href'].find("https") < 0:
                    #check if it is in a database
                    total = total+1
                    if a['href'] in array_of_ids:
                        continue  
                    array_of_ids.append(a['href'])
#                     set_trace()
                    article=requests.get(url+a['href'])
                    soup = BeautifulSoup(article.content, 'html.parser')
                    test=soup.find(class_="headline")  # link testing
                    if test is not None: # if the link is good test is not None
                        news = {} # structure for scraped data
                        news["_id"]=a['href']
                        news["source"]=url
                        news['title'] = soup.find(class_="headline").get_text()
                       
                        
                        # date format of the article is: 2 hours/minutes/days ago
                        pom = soup.find(class_="article-date").get_text()
                        pom=pom.split(" ")
                        if pom[2] == "day" or pom[2] == "days":
                            news['date']=datetime.today()-timedelta(days=int(pom[1]))
                        else:
                            news['date']=datetime.today()
                        news['date'].date()

                        #the text is composed of several smaller ones 
                        array_text=soup.find("div","article-body").find_all("p")
                        text=''

                        for t in array_text:
                            text+=t.get_text()

                        news['text']= text
#                         set_trace()
                        ReadWriteCSV.write(news)
                        successfull = successfull+1
                        
    print(total)
    print(successfull)


# In[6]:


# scraping([])


# In[ ]:




