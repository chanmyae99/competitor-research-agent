import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def google_search(query: str):
    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": 5
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()