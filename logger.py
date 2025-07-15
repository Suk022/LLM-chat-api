import csv
import os
from datetime import datetime

LOG_FILE = "chat_logs.csv"

FIELDNAMES = ["timestamp", "model", "prompt", "response", "latency", "prompt_tokens", "response_tokens"]

def log_interaction(model, prompt, response, latency, prompt_tokens, response_tokens):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),
            "model": model,
            "prompt": prompt,
            "response": response,
            "latency": latency,
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens
        }) 