import requests
import threading
import telebot
from telebot import types
import mts_hw_module.setup.config as cfg
from mts_hw_module.parsing.parsers import TeknoparkParser, MvideoParser
import mts_hw_module.database.database as db

bot = telebot.TeleBot(cfg.TOKEN)

@bot.message_handler(commands=['start'])
def send_keyboard(message, text:str='Hello, how can I help you?'):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    search_button = types.KeyboardButton(cfg.SEARCH)
    history_button = types.KeyboardButton(cfg.HISTORY)

    keyboard.add(search_button, history_button)

    if not db.check_if_user_in_base(message.from_user.id):
        bot.send_message(message.chat.id, 'Looks like you have never been here before!')

    message = bot.send_message(
        message.from_user.id,
        text=text,
        reply_markup=keyboard,
    )

    bot.register_next_step_handler(message, callback_worker)

def callback_worker(message):
    if message.text == cfg.SEARCH:
        message = bot.send_message(message.chat.id, 'Okay, let\'s search for an item')
        
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        ozon_button = types.KeyboardButton(cfg.TEKNOPARK)
        mvideo_button = types.KeyboardButton(cfg.MVIDEO)
        all_button = types.KeyboardButton(cfg.ALL)

        keyboard.add(ozon_button, mvideo_button)
        keyboard.add(all_button)

        message = bot.send_message(
            message.chat.id, 
            text='Where shall I seek?',
            reply_markup=keyboard,
        )

        bot.register_next_step_handler(message, shop_choice)
        

    elif message.text == cfg.HISTORY:
        user_requests = db.retrieve_user_requests(message.from_user.id)
        num_requests = min(len(user_requests), cfg.MAX_REQUESTS_TO_SHOW)
        
        if num_requests == 0:
            bot.send_message(message.chat.id, 'You haven\'t done any requests yet!')
        else:
            response = f'Here is your {num_requests} last requests: \n'

            for i, request in enumerate(user_requests[:num_requests]):
                response += f'{i+1}. Query: {request.search_query} Shop: {request.shop}\n'

            bot.send_message(message.chat.id, response)
        send_keyboard(message, 'Anything else I can do for you?')

    else:
        bot.send_message(message.chat.id, 'Did not understand you!')
    

def shop_choice(message):
    if message.text == cfg.MVIDEO:
        message = bot.send_message(
            message.chat.id, 
            text='What shall I seek?',
            reply_markup=types.ReplyKeyboardRemove())

        bot.register_next_step_handler(message, mvideo_handler)

    elif message.text == cfg.TEKNOPARK:
        message = bot.send_message(
            message.chat.id, 
            text='What shall I seek?',
            reply_markup=types.ReplyKeyboardRemove())

        bot.register_next_step_handler(message, teknopark_handler)

    elif message.text == cfg.ALL:
        message = bot.send_message(
            message.chat.id,
            text = 'What shall I seek?',
            reply_markup=types.ReplyKeyboardRemove())

        bot.register_next_step_handler(message, parse_all_sources)

    else:
        send_keyboard(message, 'Did not understand you!!')

def send_content(items, chat_id):
    if len(items) == 0:
        bot.send_message(chat_id, 'Sorry, nothing was found!')
    else:
        for item in items:
            response = requests.get(item.link_to_image)
            bot.send_photo(chat_id, response.content)

            text = f'Name: {item.name} \n Price: {item.price} \n Link: {item.link} \n Source: {item.shop}'
            bot.send_message(chat_id, text)

def mvideo_handler(message):
    bot.send_message(message.chat.id, 'Please wait...')
    parser = MvideoParser()
    items = parser.parse(message.text)
    send_content(items, message.chat.id)
    send_keyboard(message, 'Anything else I can do for you?')

    db.add_request_record(message.from_user.id, message.text, cfg.MVIDEO)

def teknopark_handler(message):
    bot.send_message(message.chat.id, 'Please wait...')
    parser = TeknoparkParser()
    items = parser.parse(message.text)
    send_content(items, message.chat.id)
    send_keyboard(message, 'Anything else I can do for you?')

    db.add_request_record(message.from_user.id, message.text, cfg.TEKNOPARK)

def parse_all_sources(message):
    parsers = (MvideoParser, TeknoparkParser)
    thread_list, items = [], []

    for Parser in parsers:
        parser = Parser()
        thread = threading.Thread(target=parser.parse, args=(message.text, 2, items, False))
        thread_list.append(thread,)
        thread.start()
    
    for i in range(len(thread_list)):
        thread_list[i].join()

    send_content(items, message.chat.id)
    send_keyboard(message, 'Anything else I can do for you?')
    db.add_request_record(message.from_user.id, message.text, cfg.ALL)

if __name__ == '__main__':
    print("Bot started!!")
    bot.infinity_polling()