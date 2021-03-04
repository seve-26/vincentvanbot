import telebot
import requests
from PIL import Image
import io
import os
from os.path import join, dirname
from dotenv import load_dotenv

env_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv('TG_TOKEN')
api_url = os.getenv('API_URL')

bot = telebot.TeleBot(TOKEN)
telegram_download_link = f'https://api.telegram.org/file/bot{TOKEN}/'

UNSUPPORTED_TYPES = ['audio', 'document', 'sticker', 'video', 'video_note', \
    'voice', 'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title', \
        'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', \
            'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message']

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Just send me a picture")
    
@bot.message_handler(content_types=UNSUPPORTED_TYPES)
def default_reply(message):
    bot.send_message(message.chat.id, "Unfortunately I cannot work with this data type 😢")
    bot.send_message(message.chat.id, 'Send me a picture 😅')
 
@bot.message_handler(content_types=['text'])
def reply_text(message):
    bot.reply_to(message, "I'm not very talkative. Better send me a picture 😅")


@bot.message_handler(content_types=['photo'])
def process_image(message):
    bot.reply_to(message, 'Got it! Just wait a little bit now.... 😄 🐌🐌') 

    try:
        # Prepares a photo on the Telegram API server and downloads it from there
        pic = bot.get_file(message.photo[1].file_id)
        download_url = telegram_download_link + pic.file_path  
        downloaded = requests.get(download_url)
    
        # Sends the downloaded picture to our API server
        files = {"file": (pic.file_path.split('/')[1], downloaded.content, 'image/jpeg')}
        api_response = requests.post(api_url, files=files).json()
        
        if api_response:
            # Processes a response received from our API server    
            # API stricture: {img_url, html_url, author, title, created, museum}  
            for response_item in api_response:
                pic_received = requests.get(response_item['img_url']).content
        
                # If picture is larger then 10 Mb, resize it before sending
                while (len(pic_received) > 10000000):
                    img = Image.open(io.BytesIO(pic_received))
                    img = img.resize((img.size[0] // 2, img.size[1] // 2), Image.ANTIALIAS)
            
                    byteIO = io.BytesIO()
                    img.save(byteIO, format='PNG')
                    pic_received = byteIO.getvalue()
                    
                # Sends painting and description to the chat
                bot.send_photo(message.chat.id, pic_received)
                reply = f"<i>Title:</i> {response_item['title']}\n<i>Author:</i> {response_item['author']}\n" + \
                        f"<i>Created:</i> {response_item['created']}\n<i>Museum:</i> {response_item['museum']}\n\n" + \
                        f"Link: {response_item['html_url']}"
                bot.send_message(message.chat.id, reply, disable_web_page_preview=True, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "I was not able to find similar paintings 😭")
                        
    except BaseException as e:
        print(e)
        bot.send_message(message.chat.id, 'Oops! Something crashed in the middle 🚑🤖... ')
        bot.send_message(message.chat.id, 'Please try again or use another photo 🤷🤷‍♂️')


bot.polling(none_stop=True)