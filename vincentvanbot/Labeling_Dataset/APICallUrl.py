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

def detect_labels_uri(uri, n):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image, max_results=n)
    labels = response.label_annotations
    final_custom_list = ['Illustration', 'History', 'Drawing', 'Mythology', 'Flower', 'Stock photography', 'Holy places',
                                      'Event', 'Artifact', 'Ancient history', 'Wood', 'Vintage clothing', 'Tourist attraction', 'Sculpture',
                                      'Font', 'Tree', 'Sky', 'Carving', 'Landscape', 'Metal', 'Middle ages', 'Prophet', 'Arch', 'Cloud', 'Building']   
    dict1 = {}
    final_custom_list.sort()
    result_dict = {}

    for label in labels:
        dict1[label.description]=round(label.score,2)
    print(dict1)
    
    result_dict['URL'] = uri
    for element in final_custom_list:
        if element in dict1 and dict1.get(element) > 0.6:
           result_dict[element] =  dict1.get(element) 
    return result_dict
        
    
    # if response.error.message:
    #     raise Exception(
    #         '{}\nFor more info on error messages, check: '
    #         'https://cloud.google.com/apis/design/errors'.format(
    #             response.error.message))
    
for i in range(5):
    list_of_dicts.append(detect_labels_uri(url_list[i],25))

print (list_of_dicts)
    

