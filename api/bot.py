import os
import openai
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

# Tokens de API
TELEGRAM_TOKEN = ''
OPENAI_API_KEY = ''
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

# Configuración de OpenAI
openai.api_key = OPENAI_API_KEY

# Variables globales
WELCOME_IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Google_Photos_icon_%282020%29.svg/800px-Google_Photos_icon_%282020%29.svg.png'
user_chat_mode = {}  # Usuarios en modo "chatea"
user_data = {}  # Estado de los usuarios
user_search_mode = {}  # Modo de búsqueda de fotos
user_tokens = {}  # Tokens OAuth de usuarios

# Google Drive SCOPES
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# Función para autenticar con Google Drive
def authenticate_google(user_id):
    """Autentica al usuario con Google Drive."""
    creds = None
    token_path = f'token_{user_id}.pickle'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

# Función para buscar fotos en Google Drive
def search_photos(service, query):
    """Busca fotos en Google Drive basadas en una descripción."""
    results = service.files().list(
        q=f"name contains '{query}' and mimeType contains 'image/'",
        spaces='drive',
        fields='files(id, name, webViewLink, thumbnailLink)',
        pageSize=10
    ).execute()
    return results.get('files', [])

# Comando /start
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    keyboard = [
        [InlineKeyboardButton("🔍 Buscar Fotos", callback_data='search_photos')],
        [InlineKeyboardButton("❓ Ayuda", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "¡Bienvenido al bot de Google Drive! Elige una opción:",
        reply_markup=reply_markup
    )

# Manejar búsqueda de fotos
async def handle_search_photos(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id

    if user_id not in user_tokens:
        await query.message.reply_text("🔑 Necesitas autenticarte con Google primero. Usa /auth para continuar.")
        return

    user_search_mode[user_id] = True
    await query.message.reply_text("Escribe una descripción para buscar tus fotos (por ejemplo, 'playa').")

# Procesar mensajes en modo búsqueda
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    user_message = update.message.text

    if user_id in user_search_mode:
        try:
            service = authenticate_google(user_id)
            results = search_photos(service, user_message)

            if results:
                for file in results:
                    await update.message.reply_photo(
                        photo=file['thumbnailLink'],
                        caption=f"{file['name']}\n[Ver en Drive]({file['webViewLink']})",
                        parse_mode="Markdown"
                    )
            else:
                await update.message.reply_text("No se encontraron fotos con esa descripción.")
        except Exception as e:
            await update.message.reply_text(f"Error al buscar fotos: {e}")
        finally:
            user_search_mode.pop(user_id)

# Comando /auth para autenticar con Google Drive
async def auth(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    try:
        authenticate_google(user_id)
        user_tokens[user_id] = True
        await update.message.reply_text("✅ Autenticación exitosa. Ahora puedes buscar fotos.")
    except Exception as e:
        await update.message.reply_text(f"Error al autenticar con Google: {e}")

# Comando /ayuda
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🤖 Comandos disponibles:\n"
        "/auth - Autenticar con Google Drive.\n"
        "/start - Iniciar el bot.\n"
        "Describe tus fotos para buscar en Google Drive."
    )

# Configuración principal del bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("auth", auth))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_search_photos, pattern='search_photos'))

    print("Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
