from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from api.bot_autentification import *
from api.bot_utils import *


# Comando /start
async def start(update: Update, context: CallbackContext) -> None:
    """Envía un mensaje de bienvenida con botones."""
    keyboard = [
        [InlineKeyboardButton("🔍 Buscar Fotos", callback_data='search_photos')],
        [InlineKeyboardButton("❓ Ayuda", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "¡Bienvenido al bot de Google Drive! Elige una opción:",
        reply_markup=reply_markup
    )


# Comando /auth para autenticar con Google Drive y mostrar carpetas
async def auth(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    try:
        service = authenticate_google(user_id)
        user_tokens[user_id] = True
        # Obtener carpetas del usuario
        folders = get_drive_folders(service)

        # Mostrar las carpetas al usuario
        if folders:
            folder_names = "\n".join([folder['name'] for folder in folders])
            await update.message.reply_text(f"✅ Autenticación exitosa. Tus carpetas en Google Drive:\n{folder_names}")
        else:
            await update.message.reply_text("✅ Autenticación exitosa, pero no tienes carpetas en Google Drive.")
    
    except Exception as e:
        await update.message.reply_text(f"Error al autenticar con Google: {e}")

# Comando /ayuda
async def help_command(update: Update, context: CallbackContext):
    """Envía un mensaje con los comandos disponibles."""
    await update.message.reply_text(
        "🤖 Comandos disponibles:\n"
        "/auth - Autenticar con Google Drive.\n"
        "/start - Iniciar el bot.\n"
        "Describe tus fotos para buscar en Google Drive."
    )