import requests
import os
import json
from datetime import datetime
from pathlib import Path

API_KEY = os.getenv("OPENAI_API_KEY")


def call_openai(prompt: str) -> str:
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
                "content": prompt
            }
        ],
        "temperature": 0.8
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)

    print("STATUS:", response.status_code)
    print("RAW RESPONSE:", response.text[:2000])

    response.raise_for_status()

    body = response.json()
    return body["choices"][0]["message"]["content"]


def build_prompt() -> str:
    return """
You are a professional YouTube content pack creator for a senior brain training channel.

Create a COMPLETE YouTube content package for one long-form video.

CHANNEL TYPE:
- Senior brain training
- Warm, encouraging, simple
- Audience age: 55+
- Easy English
- Positive and engaging

TOPIC:
Visual memory test / brain challenge

OUTPUT RULES:
- Return ONLY valid JSON
- Do not add markdown
- Do not use code fences
- Keep all values as plain strings except hashtags and image_prompts, which should be arrays
- The JSON keys must be exactly:

{
  "video_title_options": [
    "title 1",
    "title 2",
    "title 3",
    "title 4",
    "title 5"
  ],
  "thumbnail_text_options": [
    "thumb text 1",
    "thumb text 2",
    "thumb text 3",
    "thumb text 4",
    "thumb text 5"
  ],
  "description": "full youtube description",
  "hashtags": [
    "#tag1",
    "#tag2",
    "#tag3",
    "#tag4",
    "#tag5",
    "#tag6",
    "#tag7",
    "#tag8"
  ],
  "script": "full 10-minute video script",
  "image_prompts": [
    "prompt 1",
    "prompt 2",
    "prompt 3",
    "prompt 4",
    "prompt 5",
    "prompt 6",
    "prompt 7",
    "prompt 8",
    "prompt 9",
    "prompt 10"
  ]
}

CONTENT REQUIREMENTS:

1) video_title_options
- Give 5 clickable YouTube titles
- Senior-friendly
- Curiosity-driven
- Not too scary
- 50-70 characters preferred

2) thumbnail_text_options
- Give 5 short thumbnail text options
- 2 to 5 words each
- Large, bold, emotional
- Easy for seniors to read

3) description
- Write a clean YouTube description
- 2 short paragraphs
- Friendly CTA
- Mention brain training, memory, and fun
- Add a subscribe CTA at the end

4) hashtags
- Give exactly 8 hashtags
- Relevant to brain games, seniors, memory, quiz, wellness

5) script
- Full 10-minute long-form script
- Structure:
  - Hook
  - Intro
  - 10 questions total
  - Easy(3), Medium(4), Hard(3)
  - Score section
  - Outro
- For each question include:
  - Question
  - 5-second pause cue
  - Answer
  - Short explanation
- Minimum 900 words
- Simple English
- Warm, encouraging tone

6) image_prompts
- Give exactly 10 prompts
- One prompt per question
- Each prompt should describe a clean, colorful, senior-friendly visual
- Good for AI image generation
- No text inside image
- Horizontal 16:9 style
- Bright, clear, high contrast, easy to recognize

IMPORTANT:
Return only JSON.
""".strip()


def safe_json_parse(text: str) -> dict:
    text = text.strip()

    # Remove accidental code fences if the model includes them
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    return json.loads(text)


def save_text_file(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def save_list_file(path: Path, items: list[str]) -> None:
    cleaned = [str(item).strip() for item in items if str(item).strip()]
    path.write_text("\n".join(cleaned) + "\n", encoding="utf-8")


def save_outputs(result: dict) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("output") / f"content_pack_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    titles = result.get("video_title_options", [])
    thumbs = result.get("thumbnail_text_options", [])
    description = result.get("description", "")
    hashtags = result.get("hashtags", [])
    script = result.get("script", "")
    image_prompts = result.get("image_prompts", [])

    save_list_file(output_dir / "title.txt", titles)
    save_list_file(output_dir / "thumbnail.txt", thumbs)
    save_text_file(output_dir / "description.txt", description)
    save_list_file(output_dir / "hashtags.txt", hashtags)
    save_text_file(output_dir / "script.txt", script)
    save_list_file(output_dir / "image_prompts.txt", image_prompts)

    full_json_path = output_dir / "content_pack.json"
    full_json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return output_dir


def print_summary(output_dir: Path, result: dict) -> None:
    print("\n===== FINAL OUTPUT SUMMARY =====\n")

    print("[TITLE OPTIONS]")
    for i, title in enumerate(result.get("video_title_options", []), start=1):
        print(f"{i}. {title}")

    print("\n[THUMBNAIL TEXT OPTIONS]")
    for i, text in enumerate(result.get("thumbnail_text_options", []), start=1):
        print(f"{i}. {text}")

    print("\n[DESCRIPTION]")
    print(result.get("description", ""))

    print("\n[HASHTAGS]")
    print(" ".join(result.get("hashtags", [])))

    script_preview = result.get("script", "")[:1500]
    print("\n[SCRIPT PREVIEW]")
    print(script_preview)
    if len(result.get("script", "")) > 1500:
        print("\n... (truncated in log) ...")

    print("\n[IMAGE PROMPTS]")
    for i, prompt in enumerate(result.get("image_prompts", []), start=1):
        print(f"{i}. {prompt}")

    print(f"\nSaved folder: {output_dir}")


if __name__ == "__main__":
    prompt = build_prompt()
    raw_output = call_openai(prompt)
    parsed = safe_json_parse(raw_output)
    saved_dir = save_outputs(parsed)
    print_summary(saved_dir, parsed)
