#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import logging
import ReadWriteCSV

def scraping(array_of_ids):
    main_page = requests.get("https://www.thesun.co.uk/news/")
    main_soup = BeautifulSoup(main_page.content, 'html.parser')
    
    aovi = main_soup.find_all("a")
    successfull=0
    total=0
    oldLink=''
    
    for a in aovi:
        myLink = a['href']
        total=total+1
        #check if it is the sun and if it is longer than base link
        if myLink[0:25] != "https://www.thesun.co.uk/":
            continue
        if len(myLink) < 40:
            continue
        if oldLink == myLink:
            continue
        oldLink=myLink
        href=myLink[25:]
        if href in array_of_ids:
            continue        
        array_of_ids.append(href)
        try:
            page = requests.get(myLink)
            supa = BeautifulSoup(page.content, 'html.parser')
            news = {}
            news['title'] = supa.find(class_="article__headline").get_text()
            news['date'] = supa.find(class_="article__datestamp").get_text()+' '+supa.find(class_="article__timestamp").get_text()
            news['date'] = datetime.strptime(news['date'], '%d %b %Y, %H:%M')
            news['source'] = "https://www.thesun.co.uk"
            news['_id'] = href
            news['text'] = ''
            povi = supa.find(class_="article__content").find_all("p")
            for p in povi:
                news['text'] = news['text']+" "+p.get_text()
            
            ReadWriteCSV.write(news)    
            successfull=successfull+1
        except:
            continue

    print(successfull)
    print(total)


# In[4]:


# scraping([])


# In[ ]:




