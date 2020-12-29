#!/usr/bin/env python
# coding: utf-8

# In[ ]:


database_file = "reliable.csv"
#.path import dirname, join
import os
from os.path import join
import sys
from datetime import date
import csv
import json

def read():
    array_of_ids={}
    key1="_id"
    key2="title"
    key3="source"
    array_of_ids.setdefault(key1, [])
    array_of_ids.setdefault(key2, [])
    array_of_ids.setdefault(key3, [])
    
    path=os.path.abspath("")
    try:
        with open(join(path,database_file), 'r', encoding="utf8") as db:
            reader = csv.reader(db)
            for row in reader: 
                if row[3] == "https://www.economist.com" or \
                row[3] == "https://www.nytimes.com" and \
                (row[2].split("T"))[0] == date.today().strftime("%Y-%m-%d"):
                    array_of_ids[key1].append(row[0])
                    array_of_ids[key2].append(row[1])
                    array_of_ids[key3].append(row[3])
            jsonObj=json.dumps(array_of_ids)
    except Exception as e: 
        print(e)
    return(jsonObj)

