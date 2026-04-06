import requests
import os

API_KEY = os.getenv("OPENAI_API_KEY")

def generate():
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY is missing")

    url = "https://api.openai.com/v1/responses"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-mini",
        "input": "Say hello to J and confirm automation is working"
    }

    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()

    return res.json()["output"][0]["content"][0]["text"]

if __name__ == "__main__":
    print(generate())
