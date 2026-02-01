import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


def _extract_json(text: str):
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found in model output")
    return json.loads(match.group())


def _call_ollama(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=600
    )
    response.raise_for_status()
    return response.json()["response"]


def _normalize_questions(data: dict):
    cleaned = []

    for q in data.get("questions", []):
        q_type = q.get("type", "descriptive").lower()

        question = q.get("question", "").strip()
        answer = q.get("answer", "").strip()
        explanation = q.get("explanation", "").strip()
        options = q.get("options", [])

        # Reject incomplete questions
        if not question or not answer or not explanation:
            continue

        if q_type == "mcq" and isinstance(options, list) and len(options) == 4:
            cleaned.append({
                "type": "mcq",
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation
            })
        else:
            cleaned.append({
                "type": "descriptive",
                "question": question,
                "options": [],
                "answer": answer,
                "explanation": explanation
            })

    return {"questions": cleaned}


def generate_questions(prompt: str):
    # First attempt
    text = _call_ollama(prompt)

    try:
        raw = _extract_json(text)
    except Exception:
        # Retry once with stricter instruction
        strict_prompt = prompt + "\n\nIMPORTANT: Output ONLY raw JSON."
        text = _call_ollama(strict_prompt)
        raw = _extract_json(text)

    return _normalize_questions(raw)
