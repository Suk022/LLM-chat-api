import os
import requests

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL_MAP = {
    "mistral": "mistralai/mistral-7b-instruct",
    "llama": "meta-llama/llama-3.1-8b-instruct"
}

def send_prompt(prompt: str, model: str):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if model not in MODEL_MAP:
        raise ValueError(f"Model '{model}' not supported.")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_MAP[model],
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json() 