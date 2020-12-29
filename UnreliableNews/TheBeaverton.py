#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import logging
import ReadWriteCSV

def scraping(array_of_ids):
    start_pages=["https://www.thebeaverton.com/news/national/"]#, "https://www.thebeaverton.com/news/world/", 

    total = 0
    successfull = 0
    for start_page in start_pages:
        main_page = requests.get(start_page)
        main_soup = BeautifulSoup(main_page.content, 'html.parser')
       
        #small-12 medium-8 columns
        links = main_soup.find("div", class_="small-12 medium-8 columns").find_all("article")
        #print(linkovi)
        for link in links:
            try:
                href=link.find('a').get('href')
                total = total+1
                news = {}
                news['_id'] = href[28:]  
                #print(news['_id'])
                #check if the news is already in the db
                if news['_id'] in array_of_ids:
                    continue        
                array_of_ids.append(news['_id'])  
                
                page = requests.get(href)
                soup = BeautifulSoup(page.content, 'html.parser')


                news['title'] = soup.find(class_="entry-title").get_text()
                news['date'] = soup.find(class_="time")['datetime']#+' '+supa.find(class_="article__timestamp").get_text()
                news['date'] = datetime.fromisoformat(news['date'])
                #news['date'] = datetime.strptime(news['date'], '%d %b %Y, %H:%M')
                #print(news['date'])
                
                news['source'] = "https://www.thebeaverton.com"
                #news['_id'] = "/2019/11/new-isis-leader-torn-between-striped-tie-and-paisley-tie-for-first-day/"
                news['text'] = ''

                povi = soup.find(class_="post-content entry-content cf").find_all("p")
                for p in povi:
                    news['text'] = news['text']+" "+p.get_text()

                ReadWriteCSV.write(news)
                successfull = successfull+1
            except:   
                continue
    print(total)
    print(successfull)


# In[6]:


# scraping([])


# In[ ]:




