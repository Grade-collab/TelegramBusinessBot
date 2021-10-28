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

admin_id = 817565833
talker_id = None
queue = []


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Со скольки лет?', 'Сколько стоит?', 'Где вы находитесь?')
    keyboard.row('Связь с поддержкой')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)


@bot.message_handler(
    content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text',
                   'venue', 'video', 'video_note', 'voice'])
def send_text(message: types.Message):
    global admin_id, talker_id
    # Тут с маленькой буквы потому что lower
    #                            |
    #                            |
    if message.text == 'Связь с поддержкой':
        print("я покакал")
        if talker_id is None:
            bot.send_message(message.chat.id, 'Ищу...')
            talker_id = message.chat.id
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Закончить общение')
            bot.send_message(talker_id, 'Найдено!', reply_markup=keyboard)
            bot.send_message(admin_id, 'Найдено!', reply_markup=keyboard)

            bot.send_message(talker_id,
                             f'С вами будет общаться: {bot.get_chat(admin_id).first_name + bot.get_chat(admin_id).last_name}',
                             reply_markup=keyboard)
            bot.send_message(admin_id, f'Ваш собеседник: {message.from_user.full_name}', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Свободных операторов нет.')
            if message.chat.id not in queue:
                queue.append(message.chat.id)
                bot.send_message(message.chat.id, f'Вы в очереди вы {len(queue)}.')
            else:
                bot.send_message(message.chat.id, f'Вы уже в очереди')
    elif message.text.lower() == 'закончить общение':
        if talker_id == message.chat.id:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Со скольки лет?', 'Сколько стоит?', 'Где вы находитесь?')
            keyboard.row('Связь с поддержкой')
            bot.send_message(message.chat.id, 'Выход...', reply_markup=keyboard)
            bot.send_message(admin_id, 'Ваш опонент вышел...', reply_markup=keyboard)

            talker_id = None

            if len(queue) > 0:
                talker_id = queue.pop()
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('Закончить общение')
                bot.send_message(talker_id, 'Найдено!', reply_markup=keyboard)
                bot.send_message(admin_id, 'Найдено!', reply_markup=keyboard)

                bot.send_message(talker_id,
                                 f'С вами будет общаться: {bot.get_chat(admin_id).first_name + bot.get_chat(admin_id).last_name}',
                                 reply_markup=keyboard)
                bot.send_message(admin_id, f'Ваш собеседник: {message.from_user.full_name}', reply_markup=keyboard)

        elif message.chat.id == admin_id:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Со скольки лет?', 'Сколько стоит?', 'Где вы находитесь?')
            keyboard.row('Связь с поддержкой')
            bot.send_message(message.chat.id, 'Выход...', reply_markup=keyboard)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Со скольки лет?', 'Сколько стоит?', 'Где вы находитесь?')
            keyboard.row('Связь с поддержкой')
            bot.send_message(message.chat.id, 'Вы не общаетесь', reply_markup=keyboard)
    elif message.text.lower() == 'со скольки лет?':
        bot.send_message(message.chat.id,
                         'Мы обучаем детей с 6 до 17 лет! Группы подобраны по знаниям и возрасту учащихся.')
    elif message.text.lower() == 'сколько стоит?':
        bot.send_message(message.chat.id, 'Обучение стоит 3000 рублей в месяц.')
    elif message.text.lower() == 'где вы находитесь?':
        bot.send_message(message.chat.id,
                         'Мы находимся по адресу: Ростовская область. г.Новочеркасск. ул.Московская 20')
    else:
        if message.chat.id == talker_id or message.chat.id == admin_id:
            print(message.text, message.chat.id, talker_id, admin_id, message.id)
            if message.chat.id == admin_id:
                bot.copy_message(talker_id, admin_id, message.id)
            else:
                bot.copy_message(admin_id, talker_id, message.id)


bot.polling()
