#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import datetime
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import csv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    user = update.message.from_user
    print(user)
    update.message.reply_text(update.message.text + ", Olá ")

def my_birthday(update: Update, context: CallbackContext) -> None:
    """Write user birthday in csv"""
    if len(context.args) > 0:
        aniversario = context.args[0]
        try:
            datetime.datetime.strptime(aniversario, '%d/%m/%Y')
            user = update.message.from_user
            user_id = user.id
            user_name = user.full_name
            user_birthday = aniversario
            with open('birthdays.csv', 'a', newline='') as aniversarios:
                fieldnames = ['id','nome', 'data']
                writer = csv.DictWriter(aniversarios, fieldnames=fieldnames)
                writer.writerow({'id': user_id, 'nome': user_name, 'data': user_birthday})
            update.message.reply_text('Olá, ' + user_name + "! Eu vou lembrar do seu grande dia!")
        except ValueError:
            update.message.reply_text('Data no formato incorreto!')
    else:
        update.message.reply_text('Você deve informar uma data!')

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    arquivo = open("token.txt")
    token = arquivo.read()
    arquivo.close()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("meuaniversario", my_birthday))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()