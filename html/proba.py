#!/usr/bin/env python
# coding: utf-8

# In[2]:


# def main():
#     return "PYTHON JE ODGOVORIO"

# if __name__ == "__main__":
#     x=main()
#     return x;


# In[3]:


# pip install flask


# In[5]:


from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/proba', methods=['POST', 'GET'])
def proba():
#     name = request.args.get("name", "World")
    return "PYTHON JE ODGOVORIO"


# In[ ]:




