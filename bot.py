import random

import telebot
from pyowm.commons.exceptions import PyOWMError
from telebot import types
from telebot.types import Message

import functions
from config import TG_TOKEN, STICKER_ID

USERS = set()

print("started successfully")
bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message):
    if message.from_user.username == "ILLLIGION":
        bot.send_message(message.chat.id, "Здравствуйте, Хозяин.")
    elif message.from_user.username == "matsak_iv":
        bot.send_message(message.chat.id, "Здравствуйте, Игорь Васильевич! Напишите '/help', чтобы узнать "
                                          "список доступных команд")
    else:
        bot.send_message(message.chat.id, "Рад приветстсовать. Напишите '/type', чтобы увидеть список "
                                          "доступных комманд")
    USERS.add(message.from_user.id)


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, "Вот список доступных комманд:\n"
                                      "'/roll' - бросить один из кубиков на выбор \n "
                                      "'/id' - узнать свой Telegram ID\n"
                                      "'/weather' - узнать погоду в любом городе или стране\n"
                                      "'/time' - узнать время в любом городе или стране\n"
                                      "'/news' - узнать последние новости")


@bot.message_handler(commands=['id'])
def command_id(message):
    bot.send_message(message.chat.id, f"Ваш Telegram ID: {message.from_user.id}")


@bot.message_handler(commands=['roll'])
def command_roll(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    coin = types.KeyboardButton('Coin')
    d4 = types.KeyboardButton('D4')
    d6 = types.KeyboardButton('D6')
    d10 = types.KeyboardButton('D10')
    d20 = types.KeyboardButton('D20')
    d100 = types.KeyboardButton('D100')
    markup.add(coin, d4, d6, d10, d20, d100)
    bot.send_message(message.chat.id, "Выберите кубик на специальной клавиатуре", reply_markup=markup)


@bot.message_handler(commands=['weather'])
def command_weather(message):
    sent = bot.send_message(message.chat.id, "Напишите название города или страны")
    bot.register_next_step_handler(sent, send_forecast)


def send_forecast(message):
    try:
        functions.getweather(message.text)
    except PyOWMError:
        bot.send_message(message.chat.id, "Я не знаю такой город или страну :(\nУточните название и напишите '/weather'"
                                          "снова")
        return
    today_weather = functions.getweather(message.text)
    bot.send_message(message.chat.id,
                     f"Погода в городе {message.text} на сегодня:\nМинимальная температура: {today_weather[0]}* по "
                     f"Цельсию "
                     f"\nМаксимальная температура: {today_weather[1]}* по Цельсию"
                     f"\nТемпература на данный момент: {today_weather[2]}* по Цельсию"
                     f"\nНа небе {today_weather[3]}")


@bot.message_handler(commands=['time'])
def command_world_time(message):
    sent = bot.send_message(message.chat.id, "Напишите название города или страны")
    bot.register_next_step_handler(sent, send_time)


def send_time(message):
    try:
        functions.get_time(message.text)
    except IndexError:
        bot.send_message(message.chat.id, "Я не знаю такой город или страну :(\nУточните название и напишите "
                                          "'/world_time' снова")
        return
    time = functions.get_time(message.text)
    bot.send_message(message.chat.id, time)


@bot.message_handler(commands=['news'])
def command_news(message):
    bot.send_message(message.chat.id, "Последние новости (Источник: сайт BBC):\n")
    bot.send_message(message.chat.id, functions.get_article(), parse_mode='HTML')

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def echo_all(message):
    if "Привет" in message.text:
        bot.reply_to(message, "Уже здоровались)")
        return
    if message.text == "Coin":
        bot.reply_to(message, f"Выпало {str(random.randint(1, 2))}")
        return
    if message.text == "D4":
        bot.reply_to(message, f"Выпало {str(random.randint(1, 4))}")
        return
    if message.text == "D6":
        bot.reply_to(message, f"Выпало {str(random.randint(1, 6))}")
        return
    if message.text == "D10":
        bot.reply_to(message, f"Выпало {str(random.randint(1, 10))}")
        return
    if message.text == "D20":
        bot.reply_to(message, f"Выпало {str(random.randint(1, 20))}")
        return
    if message.text == "D100":
        bot.reply_to(message, f"Выпало {str(random.randint(1, 100))}")
        return
    else:
        bot.reply_to(message, message.text)
    USERS.add(message.from_user.id)


@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: Message):
    bot.send_sticker(message.chat.id, STICKER_ID)


bot.polling(none_stop=True)