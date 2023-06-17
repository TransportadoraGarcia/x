import logging
import re
import requests
from telegram.ext import Updater, MessageHandler, Filters

# Configurar o token do bot do Telegram
TOKEN = '5573896222:AAFLNP9PhFPX5Y7_4OOuguokpsjg70SKnVw'

# Configurar o token de API do EncurtaNet
API_TOKEN = '21ec210f636d32722482fd33e4f267451a152b84'

# canalwofc -1001316194734
# canal de filmes -1001770622838

# ID do grupo de destino
GROUP_ID = -1001770622838

# Código do sticker
STICKER_CODE = "CAACAgQAAxkBAAJQSmLS7qoxS04RewrbCpWDrCTu9tqRAAIQIAACZIo-AAF3O4xet5BxLB4E"

# Configurar o logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Adicionar console handler para exibir log no console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger('').addHandler(console_handler)

# Função para encurtar o link usando o EncurtaNet
def encurtar_link(url):
    api_url = f'https://encurta.net/api?api={API_TOKEN}&url={url}&type=1'
    response = requests.get(api_url).json()
    return response['shortenedUrl']

# Função para processar mensagens de texto e fotos
def handle_message(update, context):
    message = update.message

    if message.photo:
        # A mensagem contém uma foto
        photo = message.photo[-1]
        url = photo.get_file().file_path
        shortened_link = encurtar_link(url)
        caption = modify_text(message.caption)
        context.bot.send_photo(chat_id=GROUP_ID, photo=photo.file_id, caption=caption, reply_to_message_id=None)
    
    if message.text:
        # A mensagem contém texto
        text = message.text
        modified_text = modify_text(text)
        if modified_text:
            context.bot.send_message(chat_id=GROUP_ID, text=modified_text, reply_to_message_id=None)
        
        # Enviar o sticker
        context.bot.send_sticker(chat_id=GROUP_ID, sticker=STICKER_CODE, reply_to_message_id=None)

    # Resto do código para processar outros tipos de mensagens

def modify_text(text):
    # Procurar por URLs na mensagem
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

    # Substituir os links encurtados na mensagem
    for url in urls:
        shortened_link = encurtar_link(url)
        text = text.replace(url, shortened_link)

    return text

def main():
    # Criar o updater com o token do bot do Telegram
    updater = Updater(TOKEN, use_context=True)

    # Obter o despachante do updater
    dispatcher = updater.dispatcher

    # Registrar o handler para mensagens de texto e fotos
    message_handler = MessageHandler(Filters.text | Filters.photo, handle_message)
    dispatcher.add_handler(message_handler)

    # Iniciar o bot
    updater.start_polling()
    logging.info('Bot started')

    # Manter o bot em execução até que seja interrompido
    updater.idle()

if __name__ == '__main__':
    main()
