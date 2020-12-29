#!/usr/bin/env python
# coding: utf-8

# # The script for scraping news from  nytimes.com

# The script for srcaping one news. The result is printed, not saved in database

# In[1]:


import requests
from bs4 import BeautifulSoup
import RReadWriteCSV

page = requests.get("https://www.nytimes.com/2019/11/01/world/asia/china-student-informers.html?action=click&module=Top%20Stories&pgtype=Homepage")
sopa = BeautifulSoup(page.content, 'html.parser')

news={}
news['title'] = sopa.find("h1").get_text()
news['date'] = sopa.find("time")['datetime']
news['source'] = "https://www.nytimes.com"
news['_id'] = "/2019/11/01/world/asia/china-student-informers.html?action=click&module=Top%20Stories&pgtype=Homepage"
news['text'] = ''

var = sopa.find_all("p", class_="css-exrw3m evys1bk0")
for p in var:
    news['text'] = news['text'] + p.get_text()
    


# The links for the news are taken from "https://www.nytimes.com/section/world" <br>
# <br>
# Some links are interactive so they don't have any information. These links are being discarted.<br>
# Also if the news is already in database it is not going to be written again.

# In[3]:


import requests
from bs4 import BeautifulSoup
import RReadWriteCSV

def scraping(array_of_ids):
    count=0
    pagina = requests.get("https://www.nytimes.com/section/world")
    soup = BeautifulSoup(pagina.content, 'html.parser')
    list = soup.find(id="stream-panel")
    links = list.find_all("li")
    for link in links:
        try:
            href = link.find('a')['href']
            if href[0:12] == "/interactive":
                continue

            source = "https://www.nytimes.com" + href
            page = requests.get(source)
            soup = BeautifulSoup(page.content, 'html.parser')

            news={}
            news['_id'] = href

            if news['_id'] in array_of_ids:
                continue # ako pravi problem prvo ovo proveri     
            array_of_ids.append(news['_id'])

            news['title'] = soup.find("h1").get_text()
            news['date'] = soup.find("time")['datetime']
            news['source'] = "https://www.nytimes.com"
            news['text'] = ''

            var = soup.find_all("p", class_="css-exrw3m evys1bk0")
            for p in var:
                news['text'] = news['text'] + p.get_text()    
            count+=1
            RReadWriteCSV.write(news)
        except:
            continue
    print(count)


# In[ ]:




