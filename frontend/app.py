"""Defines Streamlit web app."""

import io
import os
import copy
import math
import requests
from os.path import join, dirname

import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from google.cloud import storage
import streamlit as st
import streamlit.components.v1 as components


def main():
    # Downloading env variables
    env_path = join(dirname(__file__),'.env')
    load_dotenv(dotenv_path=env_path)
    api_url = os.getenv('API_URL')

    # Download our catalogue
    if not os.path.exists(join(dirname(__file__),'catalog.csv')):
        storage_client = storage.Client('vincent-van-bot')
        bucket = storage_client.get_bucket('vincent-van-bot-bucket')
        blob = bucket.blob('data/catalog.csv')
        blob.download_to_filename(join(dirname(__file__),'catalog.csv'))

    # Open our catalogue + add first empty row to have empty pre-selection for a user
    db = pd.read_csv('catalog.csv', encoding='unicode_escape')
    db = db[db['FORM'] == 'painting']
    db['Title_author_date'] = db['TITLE'] + '; ' + db['AUTHOR'] + '; ' + db['DATE']
    empty_row = pd.DataFrame([[" "] * len(db.columns)], columns=db.columns)
    db = empty_row.append(db, ignore_index=True)

    # Rendering the page starts here
    st.set_page_config(page_title = 'Vincent van Bot', layout = 'wide')
    st.markdown("## Found something beautiful? Take a picture of it, upload it here, and enjoy the magic of art")
    st.markdown("")

    # Rendering the input zone
    with st.beta_expander("Input zone", expanded = True):
        input_col, _, image_col = st.beta_columns([1, 0.05, 2])

        # Left column (user input)
        with input_col:
            st.markdown("### First:")
            nsimilar = st.number_input("Choose amount of similar paintings you would like to see", value=3, min_value=1, max_value=9)
            st.markdown("### Second:")
            img = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg', 'heic'])
            st.markdown("#### or")
            st.markdown("")
            
            pic_name = st.selectbox("Tell us what is your favorite painting (and remove your downloaded pic beforehand, if any)", db['Title_author_date'])
        
        # Right column (where user pic is displayed)
        with image_col:
            st.markdown("Your picture / favorite painting:")
            img_location = st.empty()
        
        # If users downloade their own pic
        if img:
            img_copy = copy.deepcopy(img)
            img_resized = Image.open(img_copy)
            img_resized = resize_image(img_resized)
            img_location.image(img_resized)
        
        # If users enter their fav pic
        elif pic_name != " ":
            url_to_fetch = db.loc[db['Title_author_date'] == pic_name, 'URL'].values[0].replace('html','art', 1).replace('html','jpg')
            user_painting_bytes = requests.get(url_to_fetch).content
            user_painting = Image.open(io.BytesIO(user_painting_bytes))
            img_resized = resize_image(user_painting)
            img_location.image(img_resized)
        else:
            pass
            
                            
    # Just adding some spacing between input and output      
    st.markdown("")

    # Rendering output
    with st.beta_expander("You will probably like these paintings:", expanded = (img is not None or pic_name != " ")):
        # User pic
        if img:
            files = {"file": (img.name, img, img.type)}
            form_data = {"nsimilar" : nsimilar,
                         "rmfirst": False}
            render_response(api_url, files, form_data)
            
        # User's fav painting
        elif pic_name != " ":
            files = {"file": ("user_pic.jpg", user_painting_bytes, 'image/jpeg')}
            form_data = {"nsimilar" : nsimilar,
                         "rmfirst" : True}
            render_response(api_url, files, form_data)    
        else:
            pass


def render_response(api_url, file_to_send, form_data):
    
    response = requests.post(api_url, files=file_to_send, data=form_data).json()
    
    if response:
        st.markdown("")
                
        # Rendering in a grid
        n_items = len(response)
        rows = math.ceil(n_items / 3)
                            
        for n_row in range(rows):
            cols = st.beta_columns(3)
            # API stricture: {img_url, html_url, author, title, created, museum}
            for n_col in range(3 if n_row < rows - 1 else n_items - n_row * 3):
                response_item = response[3 * n_row + n_col]
                pic_received = Image.open(requests.get(response_item['img_url'], stream = True).raw)
                pic_resized = resize_image(pic_received)
                cols[n_col].markdown(f"""*Title:* [{response_item['title']}]({response_item['html_url']})  
                                            *Author:* {response_item['author']}  
                                            *Created:* {response_item['created']}  
                                            *Museum: * {response_item['museum']}""")
                cols[n_col].image(pic_resized)
                cols[n_col].markdown("")
    else:
        st.markdown("#### Looks like we were not able to find similar paintings 😭")   
        

# Custom image resize function
def resize_image(image, max_h = 500):
    pic_w, pic_h = image.size
    if pic_h <= max_h:
        return image
    
    ratio = pic_w / pic_h
    pic_h = max_h
    pic_w = int(pic_h * ratio)
    img_resized = image.resize((pic_w, pic_h))
    
    return img_resized


# Run the script
if __name__ == "__main__":
    main()
        

    
        
    
    

    

    
