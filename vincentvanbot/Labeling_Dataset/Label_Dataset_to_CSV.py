import pandas as pd
url_list = ['https://www.wga.hu/art/zzzarchi/13c/3/2/6padua12.jpg',
 'https://www.wga.hu/art/m/massys/quentin/2/ugly_duc.jpg',
 'https://www.wga.hu/art/r/rembrand/21portra/05portra.jpg',
 'https://www.wga.hu/art/m/mor/1maximi1.jpg',
 'https://www.wga.hu/art/p/ponzello/doria3.jpg',
 'https://www.wga.hu/art/c/canalett/g1/canalg10.jpg',
 'https://www.wga.hu/art/g/giovanni/rimini/life_chm.jpg',
 'https://www.wga.hu/art/zgothic/mosaics/5monreal/2transe4.jpg',
 'https://www.wga.hu/art/r/robbia/andrea/la_verna/3verna.jpg',
 'https://www.wga.hu/art/g/gericaul/1/105geric.jpg',
 'https://www.wga.hu/art/b/bellano/virgin.jpg',
 'https://www.wga.hu/art/b/bosch/5panels/11shipfo.jpg']
list_of_dicts = []

df = pd.read_csv('catalog.csv', encoding='unicode_escape')
df2 = df.head(100)
def get_jpg_link(html_link: str) -> str:
    """Tranform the html_link of the image to its respective jpg_link"""
    jpg_link = html_link.replace('html','art', 1).replace('html','jpg')
    return jpg_link

def detect_labels_df(df, n):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    from google.cloud import vision
    
    """Predefined list of Labels"""
    final_custom_list = ['Illustration', 'History', 'Drawing','Ship' , 'Flower', 'Stock photography', 'Holy places',
                         'Event', 'Artifact', 'Ancient history', 'Wood', 'Vintage clothing', 'Tourist attraction', 'Sculpture', 
                         'Font', 'Tree', 'Sky', 'Carving', 'Landscape', 'Metal', 'Middle ages', 'Prophet', 'Arch', 'Cloud', 'Building']
    final_custom_list.sort()
    
    
      
    for i in range(len(df)):

        html = df.iloc[i]["URL"]
        url = get_jpg_link(html)
        
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = url       
        response = client.label_detection(image=image, max_results=n)
        labels = response.label_annotations
        if response.error.message:
            pass
            # raise Exception(
            #     '{}\nFor more info on error messages, check: '
            #     'https://cloud.google.com/apis/design/errors'.format(
            #        response.error.message))
 
        dict_per_html = {}
        custom_label_dict = {}

        for label in labels:
            dict_per_html[label.description]=round(label.score,2)
       # print(dict_per_html)
    
        
        for element in final_custom_list:
            if element in dict_per_html and dict_per_html.get(element) > 0.6:
                custom_label_dict[element] =  dict_per_html.get(element) 
        #print(custom_label_dict)
        custom_label_dict['Index'] = i
        
        list_of_dicts.append(custom_label_dict)  
   # print(list_of_dicts)
    final_df = pd.DataFrame(list_of_dicts)
    final_df.fillna(0, inplace= True)
    final_df.set_index('Index', inplace = True)
    
    return final_df
        
    
 
detect_labels_df(df2,25).to_csv(path_or_buf='CSV.csv',index=True)
#final_df.to_csv(detect_labels_df(df2,25))
#print(detect_labels_df(df2,25))