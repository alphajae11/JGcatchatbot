import os
import requests
from dotenv import load_dotenv

load_dotenv()

CAT_API_KEY = os.getenv('CAT_API_KEY')


def get_cat_image(breed=None, count=1):
    api_url = "https://api.thecatapi.com/v1/images/search"
    params = {
        "limit": count,
        "api_key": CAT_API_KEY
    }
    if breed:
        print("Understanding breed first")
        breed_id = get_breed_id(breed)
        params["breed_id"] = breed_id

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return [image["url"] for image in data]
    except Exception as e:
        print(f"Error fetching cat image: {str(e)}")
        return []


def get_breed_id(breed):
    api_url = "https://api.thecatapi.com/v1/breeds/search"

    params = {
        "q": breed
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if len(data) > 1:
            print("Sorry we can't find the breed that you are looking for")
            return None
        return data[0]["id"]
    except Exception as e:
        print(f"Error fetching cat image: {str(e)}")
        return None
