import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

bot = telegram.Bot(token='1752020586:AAFrCK4QxnIEdVJIli1FTXGljtjEBnYT_j8')

updater = Updater(token='1752020586:AAFrCK4QxnIEdVJIli1FTXGljtjEBnYT_j8', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

def nome(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.from_user['first_name'])

name_handler = CommandHandler('nome', nome)
dispatcher.add_handler(name_handler)

updater.start_polling()