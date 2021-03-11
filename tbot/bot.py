import io
import os
import time
import requests
from PIL import Image
from os.path import join, dirname
from dotenv import load_dotenv

import pandas as pd
from google.cloud import storage
import telebot
from telebot import types

# Setting env variables
env_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv('TG_TOKEN')
api_url = os.getenv('API_URL')
api_dummy_url = os.getenv('API_DUMMY_URL')

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
db['TITLE_lowercase'] = db['TITLE'].map(str.lower)

# Starting the bot daemon
bot = telebot.TeleBot(TOKEN)
telegram_download_link = f'https://api.telegram.org/file/bot{TOKEN}/'

UNSUPPORTED_TYPES = ['audio', 'document', 'sticker', 'video', 'video_note', \
    'voice', 'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title', \
        'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', \
            'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message']

user_pic_id = ''
painting_recomm = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user_pic_id
    global painting_recomm
    
    bot.send_message(message.chat.id, "Hello! Send me a 📷 or enter your favorite painting's name")
    os.environ[str(message.chat.id) + 'DUMMY'] = ''
    user_pic_id = ''
    painting_recomm = False

@bot.message_handler(commands=['dummy'])
def switch_to_dummy(message):
    os.environ[str(message.chat.id) + 'DUMMY'] = '1'
    bot.send_message(message.chat.id, "Don't expect me to work well now 🤪🤪🤪")
    bot.send_message(message.chat.id, "But send me a picture (or painting's name)!")

@bot.message_handler(commands=['main'])
def switch_to_main(message):
    os.environ[str(message.chat.id) + 'DUMMY'] = ''
    bot.send_message(message.chat.id, "Ready for serious work again 🤓")

@bot.message_handler(commands=['which'])
def check_model(message):
    if os.getenv(str(message.chat.id) + 'DUMMY'):
        bot.send_message(message.chat.id, "Still in the dummy mode 😜")
    else:
        bot.send_message(message.chat.id, "The main mode is on! Ready to perform!")

@bot.message_handler(content_types=UNSUPPORTED_TYPES)
def default_reply(message):
    bot.send_message(message.chat.id, "Unfortunately I cannot work with this data type 😢")
    bot.send_message(message.chat.id, 'I understand only 📷 or 📝')
 
@bot.message_handler(content_types=['text'])
def reply_text(message):
    
    global user_pic_id
    global painting_recomm
        
    if not user_pic_id:
        if not painting_recomm:
            # Looks for the entered pattern in our catalogue
            suggestion_list = db.loc[db['TITLE_lowercase'].str.contains(message.text.lower()), 'Title_author_date']
            
            if not suggestion_list.empty:
                # Renders found matches in a keyboard
                markup = types.ReplyKeyboardMarkup(row_width=1)
                markup.add(*list(suggestion_list.drop_duplicates().sort_values().values[:50]))
                bot.send_message(message.chat.id, "These are pictures I cound find for your request. Choose your ❤️🖼️", reply_markup=markup)
                painting_recomm = True
                
            else:
                bot.send_message(message.chat.id, "I was not able to find paintings with such a name pattern 😭")
        else:
            # Processes user's fav painting
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "Got it and working on it! 🚀", reply_markup=markup)
            process_fav_painting(message)
            
    elif message.text not in '123456789':
        bot.send_message(message.chat.id, "Please send me a number from 1 to 9 😉")
    else:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Got it and working on it! 🚀", reply_markup=markup)
        process_image(message)


@bot.message_handler(content_types=['photo'])
def handle_message_with_photo(message):
    global user_pic_id
    user_pic_id = message.photo[1].file_id
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add(*[types.KeyboardButton(str(i)) for i in range(1, 10)])
    bot.send_message(message.chat.id, "Now please tell me how many similar paintings you'd like to find 🔢", reply_markup=markup)


def process_fav_painting(message):
    
    global user_pic_id
    global painting_recomm
        
    try:
        db_result = db.loc[db['Title_author_date'] == message.text, 'URL']
        if not db_result.empty:
            url_to_fetch = db_result.values[0].replace('html','art', 1).replace('html','jpg')
            user_painting = requests.get(url_to_fetch).content
            
            while (len(user_painting) > 10000000):
                user_painting = resize_pic(user_painting)
            
            bot.send_message(message.chat.id, "So this is your 😍 painting:")
            msg = bot.send_photo(message.chat.id, user_painting)
            user_pic_id = msg.photo[1].file_id
            
            markup = types.ReplyKeyboardMarkup(row_width=3)
            markup.add(*[types.KeyboardButton(str(i)) for i in range(1, 10)])
            bot.send_message(message.chat.id, "Now please tell me how many similar paintings you'd like to find 🔢", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Oops! Something crashed in the middle 🚑🤖... ')
            bot.send_message(message.chat.id, "I was not able to find a painting with such a description 😭")
            painting_recomm = False
            
    
    except BaseException as e:
        print(e)
        bot.send_message(message.chat.id, 'Oops! Something crashed in the middle 🚑🤖... ')
        bot.send_message(message.chat.id, 'Please try again or use another painting name 🤷🤷‍♂️')
        

def process_image(message):
    
    global user_pic_id
    global painting_recomm
    
    try:
        # Prepares a photo on the Telegram API server and downloads it from there
        pic = bot.get_file(user_pic_id)
        download_url = telegram_download_link + pic.file_path  
        downloaded = requests.get(download_url)
    
        # Sends the downloaded picture to our API server
        request_url = api_dummy_url if os.getenv(str(message.chat.id) + 'DUMMY') else api_url
        files = {"file": (pic.file_path.split('/')[1], downloaded.content, 'image/jpeg')}
        data = {"nsimilar": message.text, "rmfirst": painting_recomm}
        
        # Resetting the bot to the waiting mode
        user_pic_id = ''
        painting_recomm = False
        
        api_response = requests.post(request_url, files=files, data=data).json()
        
        if api_response:
            # Processes a response received from our API server    
            # API stricture: {img_url, html_url, author, title, created, museum}  
            returned_photos = []
            
            for response_item in api_response:
                pic_received = requests.get(response_item['img_url']).content
        
                # If picture is larger then 10 Mb, resize it before sending
                while (len(pic_received) > 10000000):
                    pic_received = resize_pic(pic_received)
                
                reply = f'<i>Title:</i> <a href="{response_item["html_url"]}">{response_item["title"]}</a>\n<i>Author:</i> {response_item["author"]}\n' + \
                        f"<i>Created:</i> {response_item['created']}\n<i>Museum:</i> {response_item['museum']}\n\n"
                    
                if len(api_response) == 1:    
                    # Sends painting and description to the chat
                    bot.send_photo(message.chat.id, pic_received, caption=reply, parse_mode = 'HTML')
                else:
                    # Or adds them to send later
                    returned_photos.append(types.InputMediaPhoto(pic_received, caption=reply, parse_mode='HTML'))
            
            # Sends group of photos
            if returned_photos:
                bot.send_media_group(message.chat.id, returned_photos)
                    
        else:
            bot.send_message(message.chat.id, "I was not able to find similar paintings 😭")
        
        time.sleep(2)
        bot.send_message(message.chat.id, "Now you can send me a 📷 or enter your ❤️🖼️ again")
                        
    except BaseException as e:
        print(e)
        bot.send_message(message.chat.id, 'Oops! Something crashed in the middle 🚑🤖... ')
        bot.send_message(message.chat.id, 'Please try again or use another photo 🤷🤷‍♂️')
        
        
def resize_pic(pic, factor = 2):
    img = Image.open(io.BytesIO(pic))
    img = img.resize((img.size[0] // factor, img.size[1] // factor), Image.ANTIALIAS)
            
    byteIO = io.BytesIO()
    img.save(byteIO, format='PNG')
    return byteIO.getvalue()

bot.polling(none_stop=True)
