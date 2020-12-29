#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
from bs4 import BeautifulSoup
import RReadWriteCSV


# In[5]:


url="https://thehill.com"


# In[6]:


def scraping(array_of_ids):
    count=0
    previous=''
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    links=soup.find_all('a', href=True)
    for a in links:
        if len(a['href']) > 50 and previous != a['href']:
            previous=a['href']
            try:
                article=requests.get(url + a['href'])
                soup = BeautifulSoup(article.content, 'html.parser')
                news={}
                news['_id']=previous
                
                if news['_id'] in array_of_ids:
                    continue    
                array_of_ids.append(news['_id'])
                
                news["source"]=url+previous
                news["title"]=soup.find(class_="content-wrapper title").find("h1").get_text()

                date=soup.find(class_="submitted-date").get_text().split(" ")
                news["date"]=date[0]
                news["text"]=''

                p_array=soup.find(class_="field-item even").find_all('p')

                for p in p_array:
                    news["text"]+=p.get_text()
                count+=1
                RReadWriteCSV.write(news)

            except:
                continue
    print(str(count) + 'scraped articles')

