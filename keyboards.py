from telebot.types import (ReplyKeyboardMarkup, KeyboardButton)


def generate_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    translate_button = KeyboardButton(text='Погода в городе')
    dictionary_button = KeyboardButton(text='Информация о стране')
    markup.add(translate_button, dictionary_button)
    return markup
