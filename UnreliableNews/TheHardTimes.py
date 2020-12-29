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
    main_page = requests.get("https://thehardtimes.net/news/")
    main_soup = BeautifulSoup(main_page.content, 'html.parser')
    
    links = []
    divs = main_soup.find(id="loop-container").findChildren("div", recursive = False)
    for div in divs:
        links.append(div.find("a")['href'])
        
    total = 0
    successfull = 0
    for link in links:
        news = {}
        news['_id'] = link[24:]
        myLink = link
        total = total + 1

        if news['_id'] in array_of_ids:
            continue        
        array_of_ids.append(news['_id'])
        
        try:
            page = requests.get(myLink)
            soup = BeautifulSoup(page.content, 'html.parser')

            news['title'] = soup.find(class_="post-title").get_text()

            news['date'] = soup.find("p", class_="post-byline").get_text().split("|")[1].strip()
            parts = news['date'].split(" ")
            if len(parts[0])<2:
                parts[0]="0"+parts[0]
            news['date'] = parts[0]+" "+parts[1]+" "+parts[2]
            news['date'] = datetime.strptime(news['date'], "%B %d, %Y")

            news['source'] = "https://thehardtimes.net"
            news['text'] = ''

            povi = soup.find(class_="post-content").find_all("p")
            for p in povi:
                news['text'] = news['text']+" "+p.get_text()

            ReadWriteCSV.write(news)  
            successfull = successfull +1
        except:
            continue

    print(successfull)
    print(total)


# In[2]:


# scraping([])


# In[ ]:




