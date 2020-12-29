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
    pagina = requests.get("https://rochdaleherald.co.uk/international/")
    sopa = BeautifulSoup(pagina.content, 'html.parser')
    
    links = []
    links.append(sopa.find(class_="td_module_mx12 td-animation-stack td-big-grid-post-0 td-big-grid-post td-small-thumb").find("a")['href'])
    divs = sopa.find(class_="td-big-grid-scroll").findChildren("div", recursive = False)
    for div in divs:
        links.append(div.find("a")['href'])
    
    total = 0
    successfull = 0
    for link in links:
        news = {}
        news['_id'] = link[28:]
        myLink = link
        total = total + 1

        if news['_id'] in array_of_ids:
            continue        
        array_of_ids.append(news['_id'])
        
        try:
            page = requests.get(myLink)
            supa = BeautifulSoup(page.content, 'html.parser')

            news['title'] = supa.find("header", class_="td-post-title").find(class_="entry-title").get_text()
            news['date'] = supa.find("time", class_="entry-date updated td-module-date")['datetime']
            news['date'] = datetime.fromisoformat(news['date'])
            news['source'] = "https://rochdaleherald.co.uk"
            news['text'] = ''
            povi = supa.find(class_="td-post-content").find_all("p")
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

