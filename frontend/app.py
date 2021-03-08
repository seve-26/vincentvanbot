import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
from PIL import Image
import copy
import pandas as pd
from google.cloud import storage

env_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path=env_path)

# Download our catalogue
if not os.path.exists('catalog.csv'):
    storage_client = storage.Client('vincent-van-bot')
    bucket = storage_client.get_bucket('vincent-van-bot-bucket')
    blob = bucket.blob('data/catalog.csv')
    blob.download_to_filename('catalog.csv')

# Open our catalogue + add first empty row to have empty pre-selection for a user
db = pd.read_csv('catalog.csv', encoding='unicode_escape')
db = db[db['FORM'] == 'painting']
db['Title_author_date'] = db['TITLE'] + '; ' + db['AUTHOR'] + '; ' + db['DATE']
empty_row = pd.DataFrame([[" "] * len(db.columns)], columns=db.columns)
db = empty_row.append(db, ignore_index=True)

#api_url = os.getenv('API_URL')
api_url = 'http://127.0.0.1:8000/uploadfile/'

# Rendering the page starts here
st.set_page_config(page_title = 'Vincent van Bot', layout = 'wide')
st.markdown("## Found something beautiful? Take a picture of it, upload it here, and enjoy the magic of art")
st.markdown("")

# Input zone
with st.beta_expander("Input zone", expanded = True):
    input_col, _, image_col = st.beta_columns([1, 0.05, 2])

    with input_col:
        st.markdown("### First:")
        nsimilar = st.number_input("Choose amount of similar paintings you would like to see", value=3, min_value=1, max_value=9)
        st.markdown("### Second:")
        #for _ in range(2): st.markdown("")
        img = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg', 'heic'])
        st.markdown("#### or")
        st.markdown("")
        
        pic_name = st.selectbox("Tell us what is your favorite painting", db['Title_author_date'])
        
        #st.button("Send")

    if img:
        img_copy = copy.deepcopy(img)
        img_resized = Image.open(img_copy)
        
        pic_w, pic_h = img_resized.size
        ratio = pic_w / pic_h
        long_vertical_pic = pic_h > 500
        
        if pic_h > 500:
            pic_h = 500
            pic_w = int(pic_h * ratio)
            img_resized = img_resized.resize((pic_w, pic_h))
        
        with image_col:
            st.markdown("Your picture / favorite painting:")
            st.image(img_resized, use_column_width = not long_vertical_pic)
        
    
if img:
    files = {"file": (img.name, img, img.type)}
    form_data = {"nsimilar" : nsimilar}
    response = requests.post(api_url, files=files, data=form_data).json()
        
    if response:
        st.markdown("")
        st.markdown("#### So you will probably like these paintings!")
        # API stricture: {img_url, html_url, author, title, created, museum}
        for response_item in response:
            st.image(response_item['img_url'])
            st.text(response_item['title'])
    else:
        st.markdown("#### We were not able to find similar paintings 😭")
            
    img = None
        
    
    

    

    
