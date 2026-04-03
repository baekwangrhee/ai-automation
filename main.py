import requests
import os

API_KEY = os.getenv("OPENAI_API_KEY")

def generate():
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY is missing")

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

    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)

    res.raise_for_status()

    body = res.json()

    if "choices" not in body:
        raise ValueError(f"Unexpected response: {body}")

    return body["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(generate())
