import spacy
import os
import json
import requests
from datetime import datetime
from collections import defaultdict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# File to store user data
user_data_file = "user_data.json"

# Weather API key
api_key = "73ea2380925e1ad9dd36944f6293a56b"


# ------------------- Utility Functions -------------------

def get_user_city():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return data.get("city", "your location")
    except:
        return "your location"


def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as f:
            return json.load(f)
    return {}


def save_user_name(name):
    user_data = load_user_data()
    user_data["name"] = name
    with open(user_data_file, "w") as f:
        json.dump(user_data, f)


def get_user_name():
    user_data = load_user_data()
    return user_data.get("name")


# ------------------- Weather Functions -------------------

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

            # Weather emoji
            condition = data['weather'][0]['main'].lower()
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
            weather_emoji = emoji_map.get(condition, "🌈")

            return (f"{weather_emoji} It's currently {temp}°C in {city} with {weather}. "
                    f"It feels like {feels_like}°C. Humidity is {humidity}% and wind speed is {wind_speed} m/s.")
        else:
            return f"Sorry, I couldn't find the weather for '{city}'."

    except Exception as e:
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
            emoji_icon = emoji_map.get(condition, "🌈")
            message += f"- {date.strftime('%A')}: {emoji_icon} {common_desc}, avg {avg_temp}°C\n"
            count += 1

        return message.strip()

    except Exception as e:
        return f"Something went wrong fetching the forecast: {str(e)}"


# ------------------- Intent & Chat Handling -------------------

def get_intent(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["forecast", "next few days", "next days", "weather next", "weather tomorrow"]):
        return "forecast"
    elif any(word in user_input for word in ["weather", "what's the weather", "how's the weather"]):
        return "weather"
    elif any(word in user_input for word in ["hello", "hi", "hey"]):
        return "greet"
    elif "your name" in user_input:
        return "ask_bot_name"
    elif "my name" in user_input or "i am" in user_input:
        return "name_input"
    elif any(word in user_input for word in ["bye", "goodbye"]):
        return "goodbye"
    else:
        return "unknown"


def get_response(user_input, waiting_for_name=False):
    user_name = get_user_name()
    intent = get_intent(user_input)

    if waiting_for_name:
        name = user_input.strip().capitalize()
        save_user_name(name)
        return f"Nice to meet you, {name}!", False

    if intent == "greet":
        if user_name:
            return f"Hello, {user_name}! How can I assist you today?", False
        else:
            return "Hello! What's your name?", True

    elif intent == "ask_bot_name":
        return "I'm LetsChat. What's your name?", True

    elif intent == "name_input":
        if "my name is" in user_input.lower():
            name = user_input.split("is")[-1].strip().capitalize()
        elif "i am" in user_input.lower():
            name = user_input.split("am")[-1].strip().capitalize()
        else:
            name = user_input.strip().capitalize()
        save_user_name(name)
        return f"Nice to meet you, {name}!", False

    elif intent == "weather":
        print("LetsChat: Would you like the weather for your current location? (yes/no)")
        confirm = input("You: ").lower()
        if "yes" in confirm:
            return get_weather(), False
        else:
            print("LetsChat: Ok, Which city?")
            city = input("You: ")
            return get_weather(city), False

    elif intent == "forecast":
        print("LetsChat: Would you like the forecast for your current location? (yes/no)")
        confirm = input("You: ").lower()
        if "yes" in confirm:
            return get_forecast(), False
        else:
            print("LetsChat: Sure! Which city?")
            city = input("You: ")
            return get_forecast(city), False

    elif intent == "goodbye":
        return f"Goodbye, {user_name or 'friend'}! Talk to you later!", False

    else:
        return "Sorry, I didn't understand that.", False


# ------------------- Main Chat Loop -------------------

def chat():
    print("LetsChat is running! (Type 'bye' to exit)")
    waiting_for_name = False
    while True:
        user_input = input("You: ")
        if "bye" in user_input.lower():
            response, _ = get_response(user_input)
            print("LetsChat:", response)
            break
        response, waiting_for_name = get_response(user_input, waiting_for_name)
        print("LetsChat:", response)


# ------------------- Run Chat -------------------

if __name__ == "__main__":
    chat()
