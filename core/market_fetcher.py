import requests

API_KEY = "ed9d428902504be4858a8711675b30d7"  # replace this


def fetch_market_news():
    url = f"https://newsapi.org/v2/everything?q=market OR supply OR inflation&language=en&pageSize=5&apiKey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])

        news_list = []

        for article in articles:
            title = article.get("title")
            if title:
                news_list.append(title)

        return news_list

    except Exception as e:
        print("❌ News fetch failed:", e)

        # fallback
        return [
            "Supply chain disruption reported",
            "Inflation increasing globally"
        ]