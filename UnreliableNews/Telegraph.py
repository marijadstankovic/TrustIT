#!/usr/bin/env python
# coding: utf-8

# In[26]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import logging
import ReadWriteCSV

def scraping(array_of_ids):
    main_page = requests.get("https://www.telegraph.co.uk/news/")
    main_soup = BeautifulSoup(main_page.content, 'html.parser')
    links = main_soup.find_all('a')

    total=0
    successfull = 0
    
    for link in links:
        myLink = "https://www.telegraph.co.uk"+link['href']
        total=total+1
        if link['href'][0:8] == "/authors":
            continue
        if link['href'][0:5] == "https":
            continue
        if len(link['href'])<16:
            continue
        

        if link['href'] in array_of_ids:
            continue
        array_of_ids.append(link['href'])
        
        try:
            page = requests.get(myLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            
            news = {}
            news['title'] = soup.find(class_="headline__heading").get_text()
            
            news['date'] = soup.find(class_="article-date-published")['datetime']            
            news['date'] = news['date'][0:16] + ":00" + news['date'][16:19] +":"+news['date'][19:]
            news['date'] = datetime.fromisoformat(news['date'])
            
            news['source'] = "https://www.telegraph.co.uk"
            
            news['_id'] = link['href']
            
            news['text'] = ''
            articles = soup.find_all(class_="component-content")
            
            breke = 0
            for article in articles:
                povi = article.find_all("p")
                for p in povi:
                    if p.get_text() == "© Telegraph Media Group Limited 2019":
                        breke = 1
                        break
                    news['text'] = news['text'] + p.get_text()
                if(breke == 1):
                    break      
            
            ReadWriteCSV.write(news)
            successfull = successfull + 1
        except:
            continue

    print(total)
    print(successfull)


# In[27]:


# scraping([])


# In[ ]:




