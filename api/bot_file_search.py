
from telegram.ext import CallbackContext
from api.bot_autentification import *
from api.bot_utils import *
from api.bot_commands import *


def search_photos(service, query):
    """Busca fotos en Google Drive basadas en una descripción."""
    try:
        # Realizamos la búsqueda en Google Drive
        results = service.files().list(
            q=f"name contains '{query}' and mimeType contains 'image/'",
            spaces='drive',
            fields='files(id, name, webViewLink, thumbnailLink)',
            pageSize=10
        ).execute()

        files = results.get('files', [])
        
        if not files:
            print("No se encontraron archivos que coincidan con la búsqueda.")
            return []

        # Verificar que thumbnailLink y id sean válidos
        for file in files:
            if 'id' not in file or not file['id']:
                print(f"Error: El archivo {file['name']} no tiene un ID válido.")
                continue

            # Si no hay thumbnailLink, asignar un valor predeterminado
            if 'thumbnailLink' not in file or not file['thumbnailLink']:
                file['thumbnailLink'] = None  # Asignar None si no hay thumbnail

        return files
    
    except Exception as e:
        print(f"Error al buscar fotos: {e}")
        return []




# Manejar búsqueda de fotos
async def handle_search_photos(update: Update, context: CallbackContext) -> None:
    """Inicia el proceso de búsqueda de fotos."""
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
    """Procesa los mensajes del usuario para buscar fotos."""
    user_id = update.message.chat_id
    user_message = update.message.text

    if user_id in user_search_mode:
        try:
            service = authenticate_google(user_id)
            results = search_photos(service, user_message)

            if results:
                # Enviar fotos encontradas
                for file in results:
                    # Si hay un enlace de miniatura, se puede usar, si no se usa una imagen predeterminada
                    image_url = file['thumbnailLink'] if file['thumbnailLink'] else 'default_image_url'

                    # Enviar la foto al chat de Telegram con el enlace a Google Drive
                    await update.message.reply_photo(
                        photo=image_url,
                        parse_mode="MarkdownV2"  # Usar MarkdownV2 para una mejor compatibilidad
                    )

            else:
                await update.message.reply_text("No se encontraron fotos con esa descripción.")
        except Exception as e:
            await update.message.reply_text(f"Error al buscar fotos: {e}")
        finally:
            user_search_mode.pop(user_id, None)

# Función para obtener las carpetas de Google Drive
def get_drive_folders(service):
    """Obtiene las carpetas del usuario en Google Drive."""
    query = "mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    return folders
