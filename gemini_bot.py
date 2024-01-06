import google.generativeai as genai
import os
from pyngrok import ngrok, conf
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO
import requests 

dotenv_path = '.env'
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
modelv = genai.GenerativeModel('gemini-pro-vision')
class GeminiBot:
    def handle_text_message(self, user_message):
        response = model.start_chat().send_message(user_message)
        reply_text = response.text
        print(reply_text)
        return reply_text

    def handle_image_message(self, image_url):
        response = requests.get(image_url, stream=True)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        # image.show()        
        response = modelv.generate_content(["Use traditional Chinese to describe the content based on this image", image], stream=True)
        response.resolve()   
        reply_text = response.text
        return reply_text