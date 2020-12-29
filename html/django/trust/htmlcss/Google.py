#!/usr/bin/env python
# coding: utf-8

# In[1]:


from serpwow.google_search_results import GoogleSearchResults
import json

# make a simple query, returning JSON
serpwow = GoogleSearchResults("2B1602EDBBCB4884BD27D8C76893A67E")

def google_API(q):
    result = serpwow.get_json({ "q" : q })

    # determine if the request was successful
    success = result["request_info"]["success"]

    if success:

      # extract the time taken and number of organic results
      search_result_count = result["search_information"]["total_results"]

      # print
      return search_result_count
#number of the results are not same as after real searching


# In[ ]:




