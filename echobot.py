import datetime
import pytz
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import csv
import math

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    #schedule jobs
    scheduledtime = datetime.time(hour=22, minute=10, tzinfo=pytz.timezone('America/Sao_Paulo'))
    context.job_queue.run_daily(callbackreminder, scheduledtime, days=(0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id)
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Opa, obrigado por me usar :), fale comigo da seguinte forma\n/meuaniversario dd/mm/aaaa - para cadastrar seu aniversário\n/listaraniversarios - Lista todos os aniversários cadastrados')
   
# def delete(user_id):

def delete(user_id):
    with open('birthdays.csv', newline='') as aniversarios:
        reader = csv.DictReader(aniversarios)
        aniversarioslist = []
        for row in reader:
            if row['id'] != user_id:
                aniversarioslist.append(row)
    with open('birthdays.csv', 'w', newline='') as aniversarios:
        fieldnames = ['id', 'nome', 'data']
        writer = csv.DictWriter(aniversarios, fieldnames=fieldnames)
        writer.writeheader()
        for linha in aniversarioslist:
            writer.writerow(linha)
            
def my_birthday(update: Update, context: CallbackContext) -> None:
    """Write user birthday in csv"""
    if len(context.args) > 0:
        aniversario = context.args[0]
        try:
            datetime.datetime.strptime(aniversario, '%d/%m/%Y')
            user = update.message.from_user
            user_id = str(user.id)
            user_name = user.full_name
            user_birthday = aniversario
            delete(user_id)
            with open('birthdays.csv', 'a', newline='') as aniversarios:
                fieldnames = ['id','nome', 'data']
                writer = csv.DictWriter(aniversarios, fieldnames=fieldnames)
                writer.writerow({'id': user_id, 'nome': user_name, 'data': user_birthday})
            update.message.reply_text('Olá, ' + user_name + "! Eu vou lembrar do seu grande dia!")
        except ValueError:
            update.message.reply_text('Data no formato incorreto!')
    else:
        update.message.reply_text('Você deve informar uma data!')

def list_birthdays(update: Update, context: CallbackContext) -> None:
    """list user birthday in csv"""
    update.message.reply_text("Os aniversários que eu sei são:\n")
    with open('birthdays.csv', newline='') as aniversarios:
        reader = csv.DictReader(aniversarios)
        aniversarioslist = []
        for row in reader:
            aniversarioslist.append(row['nome'] + " - " + row['data'] + "\n")
    aniversariospormensagem = 5
    for nmensagens in range(math.floor(len(aniversarioslist)/aniversariospormensagem)):
        mensagem = ""
        for pormensagem in range(aniversariospormensagem):
            mensagem = mensagem + aniversarioslist[5*nmensagens + pormensagem]
        context.bot.send_message(chat_id= update.effective_chat.id, text= mensagem)

    nultimasmensagens = len(aniversarioslist) % aniversariospormensagem
    mensagem = ""
    for ultimasmensagens in range(nultimasmensagens):
        mensagem = mensagem + aniversarioslist[-nultimasmensagens+ultimasmensagens]
    context.bot.send_message(chat_id= update.effective_chat.id, text= mensagem)


def callbackreminder(context):
    today = datetime.date.today()
    formated_date = today.strftime("%d/%m/%Y")
    with open('birthdays.csv', newline='') as aniversarios:
        reader = csv.DictReader(aniversarios)
        for row in reader:
            if(formated_date[0:5] == row['data'][0:5]):
                idade = int(formated_date[6:]) - int(row['data'][6:])
                context.bot.send_message(chat_id=context.job.context, text="Parabéns {0}, hoje é seu aniversário de {1} anos :)".format(row['nome'], idade))

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
    dispatcher.add_handler(CommandHandler("listaraniversarios", list_birthdays))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()