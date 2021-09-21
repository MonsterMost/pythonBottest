import requests
from telebot import TeleBot
from configs import *
from keyboards import *
from countryinfo import CountryInfo
import sqlite3 as sql

bot = TeleBot(token)
parameters = {
    'appid':'137d62f3c460fac41edca5930e84af7c',
    'units': 'metric',
    'lang': 'ru'
}



@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Здравствейте, {message.from_user.first_name}')
    buttoms(message)

def buttoms(message):
    chat_id = message.chat.id
    markup = generate_keyboard()
    msg = bot.send_message(chat_id, 'Что желаете сделать?', reply_markup=markup)
    bot.register_next_step_handler(msg, city)



def city(message):
    if message.text == 'Погода в городе':
        chat_id = message.chat.id
        city = bot.send_message(chat_id, f'Погода какого города вас интересует?')
        bot.register_next_step_handler(city, weather)
    elif message.text == 'Информация о стране':
        city = bot.send_message(message.chat.id, 'Информация о какой стране вас интересует? ')
        bot.register_next_step_handler(city, counrty_info)

# def city2(message):
#     chat_id = message.chat.id
#     city = bot.send_message(chat_id, f'Погода еще какого города вас интересует?')
#     bot.register_next_step_handler(city, weather)

def counrty_info(message):
    try:

        chat_id = message.chat.id
        country1 = CountryInfo(message.text)
        country2 = country1.info()
        print(country2)
        country = country2['altSpellings'][1]
        capital = country2['capital']
        region = country2['region']
        area = country2['area']

        db = sql.connect('countries.db')
        cursor = db.cursor()
        cursor.execute('''
        INSERT INTO info (country, capital, region, area) VALUES (?, ?, ?, ?)
        ''', (country, capital, region, area))

        bot.send_message(chat_id, f'Страна: {country},\nСтолица: {capital},\nРегион: {region},\nПлощадь: {area} кв.км')

        db.commit()
        db.close()
        buttoms(message)
    except:
        chat_id = message.chat.id
        bot.send_message(chat_id, f'Введено что-то непонятное, попробуйте заново.')
        buttoms(message)

def weather(message):
    try:
        print(message.text)
        chat_id = message.chat.id
        parameters['q'] = message.text
        response = requests.get('http://api.openweathermap.org/data/2.5/weather', parameters)
        data = response.json()

        city1 = data['name'].capitalize()
        weather = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        max_temp = data['main']['temp_max']
        min_temp = data['main']['temp_min']
        print(data)
        print(weather)
        print(temp)
        print(max_temp)
        print(min_temp)
        db = sql.connect('countries.db')

        cursor = db.cursor()
        cursor.execute('''
        INSERT INTO pogoda (city, weather, temp) VALUES (?, ?, ?)
        ''', (city1, weather, temp))
        print(cursor.fetchall())

        bot.send_message(chat_id, f'Город: {city1},\nПогода: {weather},\nТемпература: {temp} C\n')
        db.commit()
        db.close()
        buttoms(message)
    except:
        chat_id = message.chat.id
        bot.send_message(chat_id, f'Введено что-то непонятное, попробуйте заново.')
        buttoms(message)





bot.polling(none_stop=True)
