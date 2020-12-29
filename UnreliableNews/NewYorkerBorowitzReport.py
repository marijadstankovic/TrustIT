#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import logging
import ReadWriteCSV

def scraping(array_of_ids):
    pagina = requests.get("https://www.newyorker.com/humor/borowitz-report")
    sopa = BeautifulSoup(pagina.content, 'html.parser')

    lis = sopa.find(class_="River__list___2_45v").find_all("li")
    total = 0
    successfull = 0
    
    for li in lis:
        news = {}
        news['_id'] = li.find("a")['href']
        myLink = "https://www.newyorker.com" + news['_id']
        total = total + 1
        
        #https://www.newyorker.com/humor/borowitz-report/everywhere-she-went-turned-bad-says-man-with-six-bankruptcies
        
        if news['_id'] in array_of_ids:
            continue
        
        array_of_ids.append(news['_id'])
#         print(myLink)
        try:
            page = requests.get(myLink)
            supa = BeautifulSoup(page.content, 'html.parser')

            news['title'] = supa.find(class_="content-header__row content-header__hed").get_text()
#             print(news['title'])
            news['date'] = supa.find("time").get_text()
            parts = news['date'].split(" ")
            if len(parts[0])<2:
                parts[0]="0"+parts[0]
            news['date'] = parts[0]+" "+parts[1]+" "+parts[2]
            news['date'] = datetime.strptime(news['date'], "%B %d, %Y")
#             print(news['date'])

            news['source'] = "https://www.newyorker.com"
            news['text'] = ''

            povi = supa.find(class_="grid--item body body__container article__body grid-layout__content").find_all("p")
            for p in povi:
                news['text'] = news['text']+" "+p.get_text()

            ReadWriteCSV.write(news)

            successfull = successfull +1
        except:
            continue

    print(successfull)
    print(total)


# In[5]:


# scraping([])


# In[ ]:




