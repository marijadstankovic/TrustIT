#!/usr/bin/env python
# coding: utf-8

# # Scrape news articles from www.reuters.com
# 
# 
#    This script uses Python library, BeautifulSoup, for scraping.
# The infromation requested is: title, published date and text.
# All data are stored in Mongodb. Additional data which are stored in the database are: id for each article and source of article.

# In[1]:


import requests # library which will fetch the url content
from bs4 import BeautifulSoup 
from datetime import datetime
import RReadWriteCSV


# In[2]:


url = 'https://www.reuters.com' # url to scrape from


# **get_div_data function**- fuction performs the main functionality. <br>
# &emsp; **x**- the selected part of the page from which links are used <br>
# &emsp; **counter**- only first 5 links are important for the first part of the page (part_page1) <br>
# _part of the page (part_page1, part_page2)_ - includes array of divs with the same class - these divs hold a link to news that is going to be scraped

# In[4]:


def scraping(array_of_ids):
    counter=0 
    page = requests.get(url) # to get a webpage
    soup = BeautifulSoup(page.content, 'html.parser') # give a BeautifulSoup object, which represents the document                                                 # as a nested data structur
    part_page1=soup.find_all(class_="story") # class of required divs
    part_page2=soup.find_all(class_="story-photo")
    def get_div_data(x, counter):
        for b in x:  # selected div from part of the page containing the article link
            a = b.find('a', href=True)  # all <a href> links  
            if a is not None:
                article=requests.get(url+a['href']) 
                soup = BeautifulSoup(article.content, 'html.parser')
                test=soup.find(class_="ArticleHeader_headline") # link testing
                if test is not None: # if the link is good test is not None
                    news = {} # structure for scraped data
                    news['_id']=a['href'] 

                    if news['_id'] in array_of_ids:
                        continue # ako pravi problem prvo ovo proveri     
                    array_of_ids.append(news['_id'])
                    
                    news['source']=url
                    news['title'] = soup.find(class_="ArticleHeader_headline").get_text()
                    print(news['title'])

                    # date format of the article is: NOVEMBER 2, 2019 / 12:25 AM / UPDATED 19 HOURS AGO
                    pom = soup.find(class_="ArticleHeader_date").get_text().split("/")
                    news['date']=datetime.strptime(pom[0], '%B %d, %Y ')

                    #the text is composed of several smaller ones 
                    array_text=soup.find_all(class_="StandardArticleBody_body")
                    text='' 

                    for t in array_text:
                        text+=t.get_text()

                    news['text']= text

                    counter+=1
                    if(counter == 5):
                        break
                    RReadWriteCSV.write(news)
    get_div_data(part_page1, counter)
    counter=5
    get_div_data(part_page2, counter)

