#!/usr/bin/env python
# coding: utf-8

# In[16]:


import requests
from datetime import datetime
from bs4 import BeautifulSoup
import RReadWriteCSV


# In[17]:


url="https://www.vox.com/"


# In[18]:


def scraping(array_of_ids):
    count=0
    previous=''
    previousTitle=''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links=soup.find_all('a', href=True)
    for a in links:
        if "https://www.vox.com/2020" in a['href'] and previous != a['href']:
            try:
                article=requests.get(a['href'])
                soup = BeautifulSoup(article.content, 'html.parser')
                news={}
                
                news["source"]=url
                news["title"]=soup.find(class_="c-page-title").get_text()
                if previousTitle != news['title']:
                    previousTitle=news['title']
                    print(news['title'])

                    news['_id']=previousTitle
                
                    if news['_id'] in array_of_ids:
                        continue    
                    array_of_ids.append(news['_id'])
                    news['date']=soup.find("time", class_="c-byline__item")['datetime']

                    p_array=soup.find(class_="c-entry-content").find_all('p')
                    news['text']=''

                    for p in p_array:
                        news['text']+=p.get_text()
                    count+=1
                    RReadWriteCSV.write(news)
            except:
                continue
    print(str(count) + 'scraped articles')

