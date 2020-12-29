#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup
import RReadWriteCSV


# In[8]:


url="https://deadline.com/"


# In[ ]:


def scraping(array_of_ids):
    previous=''
    previousTitle=''
    count=0
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links=soup.find_all('a', href=True)

    for a in links:
        print("sto nece")
        print("")
        if "https://deadline.com/2020" in a['href'] and previous != a['href']:
            print("bla")
            previous=a['href']
            
            try:
                article=requests.get(a['href'])
                soup = BeautifulSoup(article.content, 'html.parser')
                news={}
                news["_id"]=previous
                
                if news["_id"] in array_of_ids:
                    continue # ako pravi problem prvo ovo proveri     
                array_of_ids.append(news["_id"])
                
                news["source"]=url
                news["title"]=soup.find(class_="a-article-grid__header").find("h1").get_text()
                if previousTitle != news['title']:
                    previousTitle=news['title']
                    news['date']=soup.find(class_="pmc-u-color-grey-medium-dark pmc-u-font-family-helvetica pmc-u-font-size-14").get_text()
                    p_array=soup.find(class_="a-content pmc-u-line-height-copy pmc-u-font-family-georgia pmc-u-font-size-16 pmc-u-font-size-18@desktop").find_all('p')
                    news["text"]=''
                    for p in p_array:
                        news["text"]+=p.get_text()
                    count+=1
                    RReadWriteCSV.write(news)
            except:
                print("g")
                continue
    #print(str(count) + 'scraped articles')

