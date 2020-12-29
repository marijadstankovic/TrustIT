#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import logging
import ReadWriteCSV

def scraping(array_of_ids):
    main_page = requests.get("https://www.dailysquib.co.uk/category/world")
    main_soup = BeautifulSoup(main_page.content, 'html.parser')
    
    divs = main_soup.find(class_="td-ss-main-content").find_all("div", class_="td-block-span6")
    links = []
    for div in divs:
        links.append(div.find("a")['href'])
    
    total = 0
    successfull = 0
    for link in links:
        news = {}
        news['_id'] = link[28:]
        
        if news['_id'] in array_of_ids:
            continue        
        array_of_ids.append(news['_id'])
        
        myLink = link
        total = total + 1
        
        try:            
            page = requests.get(myLink)
            soup = BeautifulSoup(page.content, 'html.parser')

            news['title'] = soup.find(class_="entry-title").get_text()
            news['date'] = soup.find("time", class_="entry-date updated td-module-date")['datetime']
            news['date'] = datetime.fromisoformat(news['date'])
            news['source'] = "https://www.dailysquib.co.uk"
            news['text'] = ''
            ps = soup.find(class_="td-post-content").find_all("p")
            for p in ps:
                news['text'] = news['text']+" "+p.get_text()

            ReadWriteCSV.write(news)    
            successfull = successfull +1
        except:
            continue
    print(successfull)
    print(total)


# In[2]:


#scraping([])


# In[ ]:




