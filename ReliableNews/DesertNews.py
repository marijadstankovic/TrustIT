#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
from bs4 import BeautifulSoup
import RReadWriteCSV


# In[6]:


def scraping(array_of_ids):
    url = 'https://www.deseret.com/latest/archives' # url to scrape from
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser') # give a BeautifulSoup object, which represents the document 
                                                      # as a nested data structure
    count=0 #count scraped pages
    adds=0
    links=soup.find_all(class_="c-entry-box--compact__title") #All links that i searching for are in this class
    for a in links:
        href=a.find('a',href=True)

        if a is not None:
            news = {} # structure for scraped data
            news["_id"]=href['href']

            if news['_id'] in array_of_ids:
                continue # ako pravi problem prvo ovo proveri     
            array_of_ids.append(news['_id'])
            article=requests.get(href['href'])
            soup=BeautifulSoup(article.content, 'html.parser')
            test=soup.find(class_="c-page-title") 
            if test is not None:
                try:                   
                    news["source"]=href['href']
                    news["title"] = test.get_text()
                    #datetime format is like: 2019-12-10T21:18:47
                    date=soup.find("time",{"class":"c-byline__item"})['datetime']
                    news["date"]=date.split("T")[0]
                    news["text"]=''

                    p_array=soup.find(class_="c-entry-content").find_all('p')
                    for p in p_array:
                        news["text"]+=p.get_text()
                    count+=1
                    RReadWriteCSV.write(news)
                except:
                    continue
    print(str(count) + 'scraped articles')
            
            
                    
                    
        

