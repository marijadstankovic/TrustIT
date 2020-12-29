#!/usr/bin/env python
# coding: utf-8

# In[3]:


from serpwow.google_search_results import GoogleSearchResults
import json

# make a simple query, returning JSON
serpwow = GoogleSearchResults("3A28F57A9E714B479C830FAD3B1032BB")

def google_API(q):
    result = serpwow.get_json({ "q" : q })

    # determine if the request was successful
    success = result["request_info"]["success"]

    if success:

      # extract the time taken and number of organic results
      search_result_count = result["search_information"]["total_results"]

      # print
      return search_result_count
# print(google_API("Trump says U.S. has 'shut down' coronavirus threat; China shuns U.S. help"))
#number of the results are not same as after real searching


# In[2]:


# pip install google-search-results-serpwow


# In[ ]:




