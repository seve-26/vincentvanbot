from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import vision
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import numpy as pd



def dummy_model(file):
    client = vision.ImageAnnotatorClient()
    contents = file.read()
    image = vision.Image(content=contents)
    response = client.label_detection(image=image, max_results = 25)
    labels = response.label_annotations
    
    final_custom_list = ['Illustration', 'History', 'Drawing', 'Mythology', 'Flower', 'Stock photography', 'Holy places',
                                      'Event', 'Artifact', 'Ancient history', 'Wood', 'Vintage clothing', 'Tourist attraction', 'Sculpture',
                                      'Font', 'Tree', 'Sky', 'Carving', 'Landscape', 'Metal', 'Middle ages', 'Prophet', 'Arch', 'Cloud', 'Building']
   '''create empty dictionary with custom labels'''
    custom_label_dict = { i : 0 for i in final_custom_list }
    google_label_dict = {}
    
    '''create dictionary with google labels and their scores'''
    for label in labels:
        google_label_dict[label.description]=round(label.score,2)
    
    '''update custom_label_dict with scores'''
    for element in final_custom_list: 
        if element in google_label_dict and google_label_dict.get(element) > 0.6:
            custom_label_dict_empty.update(element = google_label_dict(element))

    return pd.DataFrame(custom_label_dict_empty)
    
      
    
    
   # for element in final_custom_list:
       # if element in dict1 and dict1.get(element) > 0.6:
           #result_dict[element] =  dict1.get(element) 
    
    #descs = [label.description for label in labels]
    
    
    params = dict(key=api_key, cx=cx_key, q=' '.join(descs[0:5]), searchType='image')
    resp = requests.get(GOOGLE_SEARCH_API_LINK, params).json()
    
    urls = []
    for i in range(3):
        urls.append(resp['items'][i]['link'])
        
    return urls