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
    main_page = requests.get("https://babylonbee.com/news")
    main_soup = BeautifulSoup(main_page.content, 'html.parser')
    
    divs = main_soup.find("div", class_="row mb-2 gutter-4").find_all("article-card")
    success = 0
    total = 0
    for div in divs: 
        try:
            total = total+1

            news = {}
            news['_id'] = div[':path'][1:-1]
            #check if it is in the base
            if news['_id'] in array_of_ids:
                continue        
            array_of_ids.append(news['_id'])
            
            link = "https://babylonbee.com/"+news['_id']
            #get
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')

            news['title'] = soup.find(class_="large-article-title mb-1 font-weight-bold").get_text()
            #print(news['title'])
            parts = soup.find(class_="article-date mb-2").get_text().split(",")
            news['date'] = parts[0][:-2]+parts[1]
            news['date'] = datetime.strptime(news['date'], '%B %d %Y')
            #print(news['date'])
            news['source'] = "https://babylonbee.com/"
            news['text'] = ''

            ps = soup.find(class_="article-content mb-2").find_all("p")
            for p in ps:
                news['text'] = news['text']+" "+p.get_text()
            
            ReadWriteCSV.write(news)
            success = success+1
        except:
            continue
    print(success)
    print(total)


# In[2]:


#scraping([])


# In[ ]:




