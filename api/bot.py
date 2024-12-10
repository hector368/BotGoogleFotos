import openai
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Tokens de API
TELEGRAM_TOKEN = ''
OPENAI_API_KEY = ''

# Configuración de OpenAI
openai.api_key = OPENAI_API_KEY

# URL pública de una imagen en Google Fotos o un enlace directo
GOOGLE_PHOTOS_IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Google_Photos_icon_%282020%29.svg/1024px-Google_Photos_icon_%282020%29.svg.png'

# Función para interactuar con OpenAI
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Usa "gpt-3.5-turbo" si no tienes acceso a GPT-4
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error al conectar con OpenAI: {e}"

# Comando /start con imagen y mensaje de bienvenida
async def start(update: Update, context: CallbackContext):
    try:
        await update.message.reply_photo(
            photo=GOOGLE_PHOTOS_IMAGE_URL,
            caption="¡Hola! Soy tu bot conectado con OpenAI. Usa /buscar para interactuar conmigo o explora otras opciones."
        )
    except Exception as e:
        await update.message.reply_text(f"Error al cargar la imagen: {e}")

# Comando /buscar para iniciar interacción con OpenAI
async def buscar(update: Update, context: CallbackContext):
    await update.message.reply_text("¿Qué deseas buscar? Escribe tu consulta y la responderé usando OpenAI.")

# Manejar mensajes de texto (cuando el usuario usa la opción "Buscar")
async def handle_search(update: Update, context: CallbackContext):
    user_message = update.message.text  # Mensaje del usuario
    try:
        # Enviar el mensaje del usuario a OpenAI y obtener la respuesta
        openai_response = ask_openai(user_message)
        await update.message.reply_text(openai_response)  # Responder al usuario
    except Exception as e:
        await update.message.reply_text(f"Error al procesar tu mensaje: {e}")

# Comando /opciones (opcional)
async def opciones(update: Update, context: CallbackContext):
    await update.message.reply_text("Aquí están tus opciones disponibles...")

# Comando /configuracion (opcional)
async def configuracion(update: Update, context: CallbackContext):
    await update.message.reply_text("Estas son las configuraciones disponibles...")

# Comando /ayuda (opcional)
async def ayuda(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Claro! Aquí puedes obtener ayuda.")

# Configuración principal del bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Handlers para comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buscar", buscar))
    app.add_handler(CommandHandler("opciones", opciones))
    app.add_handler(CommandHandler("configuracion", configuracion))
    app.add_handler(CommandHandler("ayuda", ayuda))

    # Handler para manejar búsquedas (texto después de /buscar)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))

    print("Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
