import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# Diccionarios para gestionar estados de los usuarios
user_search_mode = {}  # Modo de búsqueda de fotos
user_tokens = {}  # Tokens OAuth de usuarios
