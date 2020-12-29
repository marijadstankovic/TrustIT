from django.shortcuts import render
import os
from os.path import dirname, join
import sys
from datetime import date
import csv
import json
from django.http import JsonResponse, HttpResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import asarray
from numpy import load
import pickle
from serpwow.google_search_results import GoogleSearchResults


# Create your views here.

def home(request):
    return render(request, 'main.html')
    
    
def read(request):
    database_file = "reliable.csv"
    array_of_ids={}
    key1="_id"
    key2="title"
    key3="source"
    array_of_ids.setdefault(key1, [])
    array_of_ids.setdefault(key2, [])
    array_of_ids.setdefault(key3, [])
    
    path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(""))))
    path=join(path, "ReliableNews")
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
        abs=json.dumps(array_of_ids)
        # jsonObj=JsonResponse({'asb':abs})
    except Exception as e: 
        print(e)
    # return render(request, 'main.html', {'array': jsonObj})
    return JsonResponse({'abs':abs})

serpwow = GoogleSearchResults("2B1602EDBBCB4884BD27D8C76893A67E")

def google_API(q):
    try:
        result = serpwow.get_json({ "q" : q })

        # determine if the request was successful
        success = result["request_info"]["success"]

        if success:

          # extract the time taken and number of organic results
          search_result_count = result["search_information"]["total_results"]

          # print
    except:
        search_result_count=-1
    return search_result_count   
    
def NN(request):
    title=request.POST.get("txtTitlet")
    text=title
    
    #getVectors
    mainDir = os.path.join(os.path.abspath(""), "NNfiles")
    vectorizerFILE = os.path.join(mainDir, "vectorizerOBJ.sav")   
    vectorizer = pickle.load(open(vectorizerFILE, "rb"))
    vectors = vectorizer.transform([text])
    adapted_vectors = vectors.toarray()
    
    #nn
    NN = pickle.load(open(os.path.join(mainDir, "NNPickles.sav"), 'rb'))
    
    # because of the specifics of the google key needed for obtaining number of search results the NN currently in use doesn't have this number as input.
    # if the google key is changed the future NN might have number of google search results as one of its inputs
    # this needs to be tested so the code works for both cases
    # THE RESULTS ARE MORE RELIABLE WITH SEARSH RESULTS AS INPUT FOR NN (NEWLY TRAINED)
    flag = False #initialy we don't use googe search results for NN
    with open(os.path.join(mainDir, "part.txt"), "r") as part:
        line = part.readline
        if line == "Y":
            flag = True
            
            
    if flag:
        x = []
        for row in adapted_vectors:
            vector = []
            for j in adapted_vectors.shape[1]:
                vector.append(row[j])
            vector.append(google_API(title))
            x.append(vector)
        result = NN.predict(x)
    else:
        result = NN.predict(adapted_vectors)
        
        #google
        search_results = google_API(title)
        if search_results is not None:
            if search_results == -1:
                m=1 #an error occured in obtaining search results. This happens as google changes the way of work very often
            elif search_results == 0:
                result[0] =0
            elif search_results <  50000:
                result[0] = result[0] - 0.1
            elif search_results < 2000000:
                result[0] = result[0] + 0.2
            if result[0] < 0:
                result[0] = 0
            if result[0] > 1:
                result[0] = 1
                
                
    result=result*100;
    result="The news is " + str(result[0]) + "% reliable." 
    
    return render( request, 'main.html', {"result": result})

















