import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import time
import requests


def get_vk(user_id):
    v = 5.131
    params = {
        'user_ids': user_id,
        'v': v, 
        'fields': 'online',
        'access_token': 'vk1.a.0jOvpqeqTeITIpdy0tEUZiaPX3PDRsBO45VtJoArcBdRcBLJVKt5XojOp_2r1kejDJHncGZWnc9yOhB_W5RvVsSGac3U1Pv-I3S_V4ePBNmBbzVMz2THFWjbjdi8fG-IzGvt4t-FqcpwFqvvSTyOxjXtR5-Ino6h7V2R0_4sgZpbSnfQL3JumpkZTYsVjIDm'
    }
    response = requests.get('https://api.vk.com/method/users.get', params=params)
    return response

def get_status(user_id):
    response = get_vk(user_id)
    status = response.json()['response'][0]['online']
    return status

def name_status(user_id):
    if get_status(user_id) == 1:
        return ' в сети'
    else:
        return 'не в сети'

def get_name(user_id):
    response = get_vk(user_id)
    first_name = response.json()['response'][0]['first_name']
    last_name = response.json()['response'][0]['last_name']
    name = first_name + ' ' + last_name
    return name



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я - нетсталкер-бот. Напиши мне ID человека в ВК и я прослежу за ним. А когда он появится в сети - я сразу же тебе напишу! (например мой ID 64886819 , а ID Оли - 75341811)")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Хорошо, человека зовут - {get_name(user_id)}')
    time.sleep(2)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Сейчас {get_name(user_id)} {name_status(user_id)} ')
    time.sleep(2)
    if get_status(user_id) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Запускаю слежение, напишу как только {get_name(user_id)} появится в сети')
        while True:
            if get_status(user_id) == 1:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{get_name(user_id)} появился в сети!!!')
                break
            else:
                time.sleep(5)



if __name__ == '__main__':
    application = ApplicationBuilder().token('5290234104:AAFAhTcfIlj0L4gC1XIPo9NntkVVcNMZfbM').build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()


