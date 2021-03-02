import requests
import os
from vincentvanbot.params import IMAGES_PATH

def download_single_image(df_row):
    response = requests.get(df_row['URL'])
    f = open(os.path.join(IMAGES_PATH,f'{df_row.name}.jpg'), 'wb')
    f.write(response.content)
    f.close()
    return df_row