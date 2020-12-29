#!/usr/bin/env python
# coding: utf-8

# # The simple script for reading ids from csv file into array
# this function will be called often

# in this variable is stored relative name of the db file

# In[1]:
from IPython.core.debugger import set_trace

database_file = "unreliable.csv"
database_new_files=[]

# to read from csv we need to import csv

# In[2]:


from os.path import dirname, join
import csv

def read():
    array_of_ids = []
    
    try:
        with open(join(dirname(__file__),database_file), 'r', encoding="utf8") as db:
            reader = csv.reader(db)
            for row in reader: #this also takes the first row => _id but
                                #it doesn't make a difference
                array_of_ids.append(row[0])
    except:
        with open(join(dirname(__file__),database_file), 'w', encoding="utf8", newline='') as db:
            writer = csv.writer(db)
            writer.writerow(["_id","title","date","source","text"])
            
    
    return(array_of_ids)


# to check if the function works just change the path:

# In[3]:


a = read()
print(len(a))


# # The simple script for writing an id into csv file

# In[4]:


from os.path import dirname, join
import csv
#, delimiter=' '  quotechar='|' , quoting=csv.QUOTE_MINIMAL
def write(row):
#     print(row["_id"])
#     print_new()
#     global database_new_files

    database_new_files.append(row)

#     if(len(database_new_files)>10):
#         dump()


# check if the function works

# In[5]:


def dump():
#     set_trace()
    print("empty")
    global database_new_files
    with open(join(dirname(__file__),database_file), 'a', encoding="utf-8", newline='') as db:
        writer = csv.writer(db)
        for row in database_new_files:
            writer.writerow([row["_id"],row["title"],row["date"],row["source"],row["text"]])
        database_new_files = []
                
             
def print_new():
    print("STAMPAM NIZ NE VECI OD 20")
    for file in database_new_files:
        print(file["title"]) #ovde se vec promeni, stampa novo zamenjeno starim???
def print_all():
    print(database_new_files)


# if some changes are made in code, the script should be downloaded as .py so the other scripts can see the change
