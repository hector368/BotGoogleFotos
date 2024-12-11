import openai
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from api.bot_autentification import *
from api.bot_utils import *
from api.bot_commands import *
from api.bot_file_search import *

# Cargar las variables de entorno


# Configuración de OpenAI
openai.api_key = OPENAI_API_KEY

# Configuración principal del bot
def main():
    """Configura y ejecuta el bot."""
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Añadir los manejadores de comandos y callback
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("auth", auth))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_search_photos, pattern='search_photos'))

    print("Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
