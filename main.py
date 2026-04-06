import requests
import os
from datetime import datetime
from pathlib import Path

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
            {
                "role": "user",
                "content": """
You are a professional YouTube script writer for a senior brain training channel.

Create a FULL 10-minute brain training video script.

TARGET AUDIENCE:
- Age 55+
- Simple English
- Easy to understand
- Encouraging and friendly tone

VIDEO STRUCTURE:

1. HOOK (0:00–0:30)
- Start with a strong attention-grabbing line

2. INTRO (0:30–1:30)
- Warm greeting
- Explain brain benefits
- Build curiosity

3. MAIN QUIZ (1:30–9:00)
- Create EXACTLY 10 questions
- Difficulty progression:
  - Easy (3)
  - Medium (4)
  - Hard (3)

Each question MUST follow this format:

Question 1:
[Clear question]

(5 seconds pause)

Answer:
[Correct answer]

Explanation:
[Short simple explanation]

4. SCORE SECTION (9:00–10:00)

- 10/10 → "Excellent memory!"
- 7–9 → "Great job!"
- 4–6 → "Good effort!"
- 0–3 → "Keep training your brain!"

STYLE RULES:
- Keep sentences short
- Use simple vocabulary
- Speak directly to the viewer
- Make it engaging and positive
- No complicated words

IMPORTANT:
- Minimum 800 words
- Clean format
- No extra explanations outside the script

TOPIC:
Visual memory test / brain challenge

OUTPUT:
Only the script
"""
            }
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    print("STATUS:", res.status_code)
    print("RAW RESPONSE:", res.text)
    res.raise_for_status()

    return res.json()["choices"][0]["message"]["content"]

def save_script(text: str) -> str:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = output_dir / f"brain_script_{timestamp}.txt"

    filename.write_text(text, encoding="utf-8")
    return str(filename)

if __name__ == "__main__":
    result = generate()
    saved_path = save_script(result)

    print("\n\n===== FINAL OUTPUT =====\n")
    print(result)
    print(f"\n\nSaved to: {saved_path}")
