from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
import os

# Token de bot (debe ser almacenado de manera segura)
TOKEN = '7593679019:AAHCSuzxkkVG6PSHaicWVYuh0yequ_x-5jc'
# Mensajes y opciones
START_MESSAGE = "¡Hola! Soy tu bot de Telegram. Selecciona una opción:"


# Comando inicial
async def start(update: Update, context: CallbackContext):
    try:
        # Crear el teclado con botones
        keyboard = [
            [KeyboardButton(" Opciones"), KeyboardButton(" Buscar")],
            [KeyboardButton(" Configuración"), KeyboardButton(" Ayuda")],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        # Enviar el mensaje inicial con el menú
        await update.message.reply_text(START_MESSAGE, reply_markup=reply_markup)
    except Exception as e:
        await update.message.reply_text("Error al iniciar el bot.")
        print(f"Error: {e}")


# Manejar mensajes de texto
async def handle_message(update: Update, context: CallbackContext):
    try:
        user_message = update.message.text

        # Respuestas basadas en el botón seleccionado
        if user_message == " Opciones":
            await update.message.reply_text("Aquí están tus opciones disponibles...")
        elif user_message == " Buscar":
            await update.message.reply_text("¿Qué deseas buscar? Escribe algo.")
        elif user_message == " Configuración":
            await update.message.reply_text("Estas son las configuraciones disponibles...")
        elif user_message == " Ayuda":
            await update.message.reply_text("¡Claro! Aquí puedes obtener ayuda.")
        else:
            await update.message.reply_text(f"Recibí tu mensaje: {user_message}")
    except Exception as e:
        await update.message.reply_text("Error al procesar el mensaje.")
        print(f"Error: {e}")


# Configuración de handlers
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers para comandos y mensajes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot en ejecución...")
    app.run_polling()


if __name__ == "__main__":
    main()