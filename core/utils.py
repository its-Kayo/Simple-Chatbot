import os
import json
import requests
import logging

user_data_file = "user_data.json"

def get_user_city():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return data.get("city", "your location")
    except Exception as e:
        logging.error("Error in get_user_city: %s", str(e))
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

def reset_user_data():
    if os.path.exists(user_data_file):
        os.remove(user_data_file)

def get_user_name():
    user_data = load_user_data()
    return user_data.get("name")
