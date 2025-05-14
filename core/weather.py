import requests
import logging
from datetime import datetime
from collections import defaultdict
from .utils import get_user_city

api_key = "73ea2380925e1ad9dd36944f6293a56b"

emoji_map = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧",
    "drizzle": "🌦",
    "thunderstorm": "🌩",
    "snow": "🌨",
    "mist": "🌫",
    "fog": "🌫"
}

def get_weather(city=None):
    if not city:
        city = get_user_city()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = data['weather'][0]['description'].capitalize()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            condition = data['weather'][0]['main'].lower()
            emoji = emoji_map.get(condition, "🌈")

            return (f"{emoji} It's currently {temp}°C in {city} with {weather}. "
                    f"It feels like {feels_like}°C. Humidity is {humidity}% and wind speed is {wind_speed} m/s.")
        else:
            return f"Sorry, I couldn't find the weather for '{city}'."
    except Exception as e:
        logging.error("Error in get_weather: %s", str(e))
        return f"Oops! Something went wrong: {str(e)}"

def get_forecast(city=None):
    if not city:
        city = get_user_city()

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return f"Sorry, I couldn't get the forecast for '{city}'."

        forecast_data = data["list"]
        daily_forecast = defaultdict(list)

        for entry in forecast_data:
            date = datetime.fromtimestamp(entry["dt"]).date()
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["description"]
            daily_forecast[date].append((temp, desc))

        message = f"🌤️ 3-day forecast for {city}:\n"
        count = 0
        for date, entries in daily_forecast.items():
            if count == 3:
                break
            temps = [t[0] for t in entries]
            descriptions = [d[1] for d in entries]
            avg_temp = round(sum(temps) / len(temps), 1)
            common_desc = max(set(descriptions), key=descriptions.count)
            condition = common_desc.lower().split()[0]
            emoji = emoji_map.get(condition, "🌈")
            message += f"- {date.strftime('%A')}: {emoji} {common_desc}, avg {avg_temp}°C\n"
            count += 1

        return message.strip()
    except Exception as e:
        logging.error("Error in get_forecast: %s", str(e))
        return f"Something went wrong fetching the forecast: {str(e)}"
