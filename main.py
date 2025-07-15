import os
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openrouter_client import send_prompt
import time
from logger import log_interaction
from datetime import datetime
import pytz

load_dotenv()


app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str
    model: str

@app.get("/")
def root():
    return {"message": "LLM Chat API is running. See /docs for API documentation."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    start_time = time.time()
    try:
        response = send_prompt(request.prompt, request.model)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model API error: {e}")
    latency = time.time() - start_time


    # for extracting model response text
    try:
        model_reply = response["choices"][0]["message"]["content"]
    except Exception:
        model_reply = str(response)
    
    # to get Simple token count (word count as proxy)
    prompt_tokens = len(request.prompt.split())
    response_tokens = len(model_reply.split())
    
    # to log interaction
    log_interaction(request.model, request.prompt, model_reply, latency, prompt_tokens, response_tokens)

    now = datetime.now(pytz.timezone('Asia/Kolkata'))  
    formatted_timestamp = now.strftime("%H:%M %B %d,%Y")
    return {
        "response": model_reply,
        "latency": latency,
        "prompt_tokens": prompt_tokens,
        "response_tokens": response_tokens,
        "model": request.model,
        "timestamp": formatted_timestamp
    } 