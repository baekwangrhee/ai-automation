import requests
import os

API_KEY = os.getenv("OPENAI_API_KEY")

def generate():
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": "Give me 1 brain quiz for seniors"}
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(generate())
