# bebrostan_bot 2021
# Coded by Ender (@TheEnderOfficial)
# And by Grade-Collab (@Grade-Collab)

import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)
freeid = None

users = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Искать')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global freeid
    # Тут с маленькой буквы потому что lower
    #                            |
    #                            |
    if message.text.lower() == 'искать':

        if message.chat.id not in users:
            bot.send_message(message.chat.id, 'Ищю...')

            if freeid is None:
                freeid = message.chat.id
            else:
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('Закончить общение')
                bot.send_message(message.chat.id, 'Найдено!', reply_markup=keyboard)
                bot.send_message(freeid, 'Найдено!', reply_markup=keyboard)

                users[freeid] = message.chat.id
                users[message.chat.id] = freeid
                freeid = None

            print(users, freeid)
        else:
            bot.send_message(message.chat.id, 'Не найдено.')
    elif message.text.lower() == 'закончить общение':
        if message.chat.id in users:
            bot.send_message(message.chat.id, 'Выход...')
            bot.send_message(users[message.chat.id], 'Ваш опонент вышел...')

            del users[users[message.chat.id]]
            del users[message.chat.id]

            print(users, freeid)
        elif message.chat.id == freeid:
            bot.send_message(message.chat.id, 'Выход...')
            freeid = None

            print(users, freeid)
        else:
            bot.send_message(message.chat.id, 'Вы не в поиске!')


@bot.message_handler(
    content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text',
                   'venue', 'video', 'video_note', 'voice'])
def chatting(message: types.Message):
    if message.chat.id in users:
        bot.copy_message(users[message.chat.id], users[users[message.chat.id]], message.id)


bot.polling()
