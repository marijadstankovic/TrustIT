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


# In[11]:

import flask
from flask import Flask, escape, request
from bokeh.embed import json_item
from bokeh.plotting import figure
import json
from bokeh.io import curdoc, show
from bokeh.layouts import column, layout
from bokeh.models import TextAreaInput, Button, ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure
from bokeh.resources import CDN
from os.path import dirname, join
from jinja2 import Template

app = Flask(__name__)

page = Template(open(join(dirname(__file__), "template/main.html")).read())
@app.route('/', methods=["GET", "POST"])
def root():
    return page.render(resources=CDN.render())
@app.route('/pr', methods=["GET", "POST"])

def proba():
#     name = request.args.get("name", "World")
    plot = figure(plot_height=400, plot_width=500, sizing_mode="scale_both")
    source = ColumnDataSource(data=dict(x=[], y=[]))
    source.data = dict(x=[1,2,3,100], y=[1,2,3,100])
    plot.circle(x="x", y="y", source = source)
    objekat ={}
    objekat["graf"] = json_item(plot, "myplot")
    objekat["predict"] = 56
    
    return json.dumps(objekat)#json.dumps(json_item(objekat, "myplot"))


# In[12]:


proba()


# In[ ]:




