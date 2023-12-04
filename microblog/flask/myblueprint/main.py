from flask import Blueprint, request, render_template, g, session, redirect, url_for
import requests
import datetime
import math

API_KEY = 'ce3e3d8feefd305c5c0245a75daec24b'

main_bp = Blueprint(
    'main_blueprint', __name__,
)

city_dict = {
    "Moscow": 'Москва',
    "London": 'Лондон',
    "Tokyo": 'Токио'
}

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


def weather_cast_post(request):


    city = request.form.get('city')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={API_KEY}"
    response = requests.get(url=url)
    data = response.json()
    cur_temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    print(response.json())

    sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"])
    print("Обработка POST-запроса")
    context = {
        'cur_temp': cur_temp,
        'humidity': humidity,
        'pressure': pressure,
        'wind': wind,
        'length_of_the_day': length_of_the_day,
        'sunrise_timestamp': sunrise_timestamp,
        'sunset_timestamp': sunset_timestamp,
        'city_dict': city_dict,
        'selected_city': city
    }
    return render_template(
        "weather.html",
        context=context
    )


@main_bp.route('/weather_cast', methods=['POST', 'GET'])
def weather_cast():

    if request.method == 'POST':
        return weather_cast_post(request)
    # ПОГОДА

    city = "Moscow"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={API_KEY}"
    response = requests.get(url=url)
    data = response.json()
    cur_temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    print(response.json())

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
        'city_dict': city_dict,
        'title': "Home",

    }
    return render_template(
        "weather.html",
        context=context
    )
