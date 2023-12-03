from flask import Blueprint, request, render_template, g, session, redirect, url_for
import requests
import datetime
import math

API_KEY = 'ce3e3d8feefd305c5c0245a75daec24b'

main_bp = Blueprint(
    'main_blueprint', __name__,
)


@main_bp.route('/', methods=['POST', 'GET'])
@main_bp.route('/main', methods=['POST', 'GET'])
def main_view():
    return "Hello world bitch"


@main_bp.route('/index')
def index():
    user = {'nickname': 'Сиделец'}  # выдуманный пользователь
    posts = [  # список выдуманных постов
        {
            'author': {'nickname': 'Леха Сиплый'},
            'body': 'я вор'
        },
        {
            'author': {'nickname': 'Старший'},
            'body': 'Вилкой в глаз или в жопу раз?'
        }
    ]

    context = {
        'posts': posts,
        'user': user,
        'title': "Home",

    }
    return render_template(
        "index.html",
        context=context
    )


@main_bp.route('/weather_cast')
def weather_cast():
    # ПОГОДА

    city = input('Введите город: ')

    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&lang=ru&units=metric&appid=" + API_KEY)
    data = response.json()
    cur_temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]

    sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

    # продолжительность дня
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"])

    weather = (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\nПогода в городе: {city}\n"
               f"Температура: {cur_temp}°C\nВлажность: {humidity}%\n"
               f"Давление: {math.ceil(pressure / 1.333)} мм.рт.ст\n"
               f"Ветер: {wind} м/с \nВосход солнца: {sunrise_timestamp}\n"
               f"Закат солнца: {sunset_timestamp}\n"
               f"Продолжительность дня: {length_of_the_day}\n"
               f"Хорошего дня!")

    context = {
        'response': response,
        'data': data,
        'city': city,
        'cur_temp': cur_temp,
        'humidity': humidity,
        'pressure': pressure,
        'wind': wind,
        'length_of_the_day': length_of_the_day,
        'sunrise_timestamp': sunrise_timestamp,
        'sunset_timestamp': sunset_timestamp,
        'weather': weather,
        'title': "Home",

    }
    return render_template(
        "weather.html",
        context=context
    )
