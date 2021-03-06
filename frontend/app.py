import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
#from PIL import Image
#import copy

env_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path=env_path)

api_url = os.getenv('API_URL')

st.markdown("#### Found something beautiful? Take a picture of it, upload it here, and enjoy the magic of art")
img = st.file_uploader('Please upload an image', type=['png', 'jpg', 'jpeg', 'heic'])
#img_copy = copy.deepcopy(img)

if img:
    #img_resized = Image.open(img_copy).resize((300, 300))
    st.markdown("#### You have uploaded this picture:")
    st.image(img)
    
    files = {"file": (img.name, img, img.type)}
    response = requests.post(api_url, files=files).json()
    
    if response:
        st.markdown("#### So you will probably like these paintings!")
        # API stricture: {img_url, html_url, author, title, created, museum}
        for response_item in response:
            st.image(response_item['img_url'])
    else:
        st.markdown("#### We were not able to find similar paintings 😭")
    
    
    

    

    
