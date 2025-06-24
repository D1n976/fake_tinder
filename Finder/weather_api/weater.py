import requests
import utils.utils as ut
import json

def get_weather_of_city(city) :
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={ut.config['api']['weather_api']}&units=metric"
    response = requests.get(url)
    print(response)
    data = response.json()
    city = data['name']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description']
    return (f"Погода в {city}:\n"
            f"Температура: {temp}°C\n"        f"Ощущается как: {feels_like}°C\n"
            f"Влажность: {humidity}%\n"        f"Скорость ветра: {wind_speed} м/с\n"
            f"Описание: {description}")

def get_weather_of_location(lat, lon) :
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={ut.config['api']['weather_api']}'
    response = requests.get(url)
    data = response.json()
    city = data['name']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description']
    return(f"Погода в {city}:\n"
          f"Температура: {temp}°C\n"        f"Ощущается как: {feels_like}°C\n"
          f"Влажность: {humidity}%\n"        f"Скорость ветра: {wind_speed} м/с\n"
          f"Описание: {description}")

def get_countries() :
    with open('temp/countries.json') as f :
        reader = json.load(f)
        return [x['country'] for x in reader]

def get_city_by_country(country):
    with open('temp/countries.json') as f:
        reader = json.load(f)
        return [x['cities'] for x in reader if x['country'] == country][0]