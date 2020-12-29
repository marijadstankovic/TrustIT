#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import logging
import ReadWriteCSV

def scraping(array_of_ids):
    main_page = requests.get("https://chaser.com.au/")
    main_soup = BeautifulSoup(main_page.content, 'html.parser')
    
    links = []
    table_row = main_soup.find("div", class_="table row_1").find_all("a")
    for a in table_row:
        links.append(a['href'])
    table_row = main_soup.find("div", class_="table row_2").find_all("a")
    for a in table_row:
        links.append(a['href'])
        
    total = 0
    successfull = 0
    for link in links:
        news = {}
        news['_id'] = link[21:]
        
        if news['_id'] in array_of_ids:
            continue
        array_of_ids.append(news['_id'])
        
        myLink = link
        total = total + 1
        
        try:
            page = requests.get(myLink)
            soap = BeautifulSoup(page.content, 'html.parser')

            news['title'] = soap.find(class_="title_title").get_text()
            news['date'] = soap.find("time", class_="entry-date")['datetime']
            news['date'] = datetime.fromisoformat(news['date'])
            news['source'] = "https://chaser.com.au"
            news['text'] = ''

            ps = soap.find("article").findChildren("p", recursive = False)
            #print(ps[0].get_text().split("fusetag")[0].strip())
            i=0
            for p in ps:
                try:
                    if i==0:
                        news['text'] = news['text']+" "+p.get_text().split("fusetag")[0].strip()
                    else:
                        news['text'] = news['text']+" "+p.get_text()
                    i=i+1

                except:
                    continue

            ReadWriteCSV.write(news)
            successfull = successfull +1
        except:
            continue
    print(successfull)
    print(total)


# In[ ]:


# scraping(ReadWriteCSV.read())

