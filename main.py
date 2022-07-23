import os

import telebot
from telebot import types

import config as cfg

bot = telebot.TeleBot(cfg.TOKEN)

@bot.message_handler(commands=['start'])
def hello_message(message, text:str='Hello, how can I help you?'):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    search_button = types.KeyboardButton(cfg.SEARCH)
    history_button = types.KeyboardButton(cfg.HISTORY)

    keyboard.add(search_button, history_button)

    message = bot.send_message(
        message.from_user.id,
        text=text,
        reply_markup=keyboard,
    )

    bot.register_next_step_handler(message, callback_worker)

def callback_worker(message):
    if message.text == cfg.SEARCH:
        message = bot.send_message(message.chat.id, 'Okay, let\'s search for an item')
        bot.register_next_step_handler(message, choose_shop)

    elif message.text == cfg.HISTORY:
        bot.register_next_step_handler(message, show_history)

def choose_shop(message, text:str='Please choose search options:'):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    ozon_button = types.KeyboardButton(cfg.OZON)
    mvideo_button = types.KeyboardButton(cfg.MVIDEO)
    wb_button = types.KeyboardButton(cfg.WB)
    all_button = types.KeyboardButton(cfg.ALL)

    keyboard.add(ozon_button, mvideo_button)
    keyboard.add(wb_button, all_button)

    message = bot.send_message(
        message.from_user.id, 
        text=text,
        reply_markup=keyboard,
    )

    bot.register_next_step_handler(message, search_logic)

def search_logic(message):
    raise NotImplementedError

def show_history(message):
    raise NotImplementedError

@bot.message_handler(content_types='text')
def get_item_name(message):
    bot.send_message(message.chat.id, f'Got item: {message.text}')


if __name__ == '__main__':
    print("Bot started!!")
    bot.infinity_polling()

