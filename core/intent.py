from core.weather import get_weather, get_forecast
from core.utils import get_user_name, save_user_name, reset_user_data
from core.news import get_top_headlines

INTENTS = {
    "forecast": ["forecast", "next few days", "weather next", "weather tomorrow"],
    "weather": ["weather", "what's the weather", "how's the weather"],
    "greet": ["hello", "hi", "hey"],
    "ask_bot_name": ["your name"],
    "name_input": ["my name", "i am"],
    "goodbye": ["bye", "goodbye"],
    "reset": ["reset"],
    "help": ["help"],
    "news": ["news", "headlines", "latest news", "top news"]
}

def get_intent(user_input):
    user_input = user_input.lower()
    for intent, keywords in INTENTS.items():
        if any(word in user_input for word in keywords):
            return intent
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

    elif intent == "reset":
        reset_user_data()
        return "Your data has been reset. Let's start over!", True

    elif intent == "help":
        return ("You can ask about the weather, forecast, or tell me your name! "
                "Try: 'What's the weather like?' or 'My name is Alex'."), False

    elif intent == "weather":
        print("LetsChat: Would you like the weather for your current location? (yes/no)")
        confirm = input("You: ").lower()
        if "yes" in confirm:
            return get_weather(), False
        else:
            print("LetsChat: Ok, Which city?")
            city = input("You: ").strip()
            if not city:
                return "Please enter a valid city name.", False
            return get_weather(city), False

    elif intent == "forecast":
        print("LetsChat: Would you like the forecast for your current location? (yes/no)")
        confirm = input("You: ").lower()
        if "yes" in confirm:
            return get_forecast(), False
        else:
            print("LetsChat: Sure! Which city?")
            city = input("You: ").strip()
            if not city:
                return "Please enter a valid city name.", False
            return get_forecast(city), False

    elif intent == "news":
        return get_top_headlines(), False

    elif intent == "goodbye":
        return f"Goodbye, {user_name or 'friend'}! Talk to you later!", False

    else:
        return ("I'm not sure I understood that. Try asking about the weather, forecast, or introduce yourself."), False
