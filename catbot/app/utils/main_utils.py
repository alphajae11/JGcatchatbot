import requests
from .assistantcatbot import chat_with_cat_bot
from .cat_image import get_cat_image
from PIL import Image
from io import BytesIO


def process_chat(message):
    return chat_with_cat_bot(message, get_cat_image)


def show_cat_images(image_urls):
    for url in image_urls:
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.show()
        except Exception as e:
            print(f"Error displaying image: {str(e)}")

