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
    keyboard.row('Со скольки лет?', 'Сколько стоит?', 'Где вы находитесь?')
    keyboard.row('Связь с поддержкой')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message: types.Message):
    global freeid
    # Тут с маленькой буквы потому что lower
    #                            |
    #                            |
    if message.text.lower() == 'cвязь с поддержкой':

        if message.chat.id not in users:
            bot.send_message(message.chat.id, 'Ищю...')

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Закончить общение')
            bot.send_message(message.chat.id, 'Найдено!', reply_markup=keyboard)
            bot.send_message(freeid, 'Найдено!', reply_markup=keyboard)

            bot.send_message(message.chat.id,
                             f'С вами будет общатся: {bot.get_chat(freeid).first_name + bot.get_chat(freeid).last_name}',
                             reply_markup=keyboard)
            bot.send_message(freeid, f'Ваш собеседник: {message.from_user.full_name}', reply_markup=keyboard)

            users[freeid] = message.chat.id
            users[message.chat.id] = freeid
            freeid = None
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
    elif message.text.lower() == 'со скольки лет?':
        bot.send_message(message.chat.id,
                         'Мы обучаем детей с 6 до 17 лет! Группы подобраны по знаниям и возрасту учащихся.')
    elif message.text.lower() == 'сколько стоит?':
        bot.send_message(message.chat.id, 'Обучение стоит 3000 рублей в месяц.')
    if message.text.lower() == 'где вы находитесь?':
        bot.send_message(message.chat.id,
                         'Мы находимся по адресу: Ростовская область. г.Новочеркасск. ул.Московская 20')


@bot.message_handler(
    content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text',
                   'venue', 'video', 'video_note', 'voice'])
def chatting(message: types.Message):
    if message.chat.id in users:
        bot.copy_message(users[message.chat.id], users[users[message.chat.id]], message.id)


bot.polling()
