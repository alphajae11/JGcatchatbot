import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    CAT_API_KEY = os.environ.get('CAT_API_KEY')
