import os
import requests
import logging





def get_top_headlines(country="us", category=None):
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        return "News API key is not set. Please set NEWS_API_KEY in your environment."

    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={NEWS_API_KEY}"
    if category:
        url += f"&category={category}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] != "ok":
            return "Sorry, I couldn't fetch the news at the moment."

        articles = data["articles"][:5]
        if not articles:
            return "No news articles found."

        message = "🗞️ Top News Headlines:\n"
        for article in articles:
            message += f"- {article['title']} ({article['source']['name']})\n"

        return message.strip()

    except Exception as e:
        logging.error("Error in get_top_headlines: %s", str(e))
        return f"Error fetching news: {str(e)}"
