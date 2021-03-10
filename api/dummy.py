import os
import requests
from dotenv import load_dotenv
from os.path import join, dirname

from google.cloud import vision


# Setting env variables
GOOGLE_SEARCH_API_LINK='https://customsearch.googleapis.com/customsearch/v1'
env_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('API_KEY')
cx_key = os.getenv('CX_KEY')

# Being used until we make our own model work
def dummy_model(database, file, n_similar=3):
    
    client = vision.ImageAnnotatorClient()

    contents = file.read()
    image = vision.Image(content=contents)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    descs = [label.description for label in labels]

    params = dict(key=api_key, cx=cx_key, q=' '.join(descs[0:2]), \
        siteSearch='https://www.wga.hu', siteSearchFilter='i', searchType='image', \
            exactTerms='searchable fine arts image database')

    resp = requests.get(GOOGLE_SEARCH_API_LINK, params).json()
    if resp['searchInformation']['totalResults'] == '0': 
        return []

    response = []
    
    for item in resp['items']:
        link = item['link']
        if '/art/' not in link:
            continue

        context_link = item['image']['contextLink']
        if context_link not in set(database['URL']):
            continue

        response_item = dict (img_url = link, html_url = context_link, \
                              author = database.loc[database['URL'] == context_link, 'AUTHOR'].values[0], \
                              title = database.loc[database['URL'] == context_link, 'TITLE'].values[0], \
                              created = database.loc[database['URL'] == context_link, 'DATE'].values[0], \
                              museum = database.loc[database['URL'] == context_link, 'LOCATION'].values[0])

        response.append(response_item)

        if len(response) == n_similar:
            break

    return response