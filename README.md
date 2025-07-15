# Multi-Model LLM Chat Service Backend
This project is a minimal FastAPI service that lets you chat with two open-source LLMs (Mistral-7B and Llama-3.1-8B Instruct) via OpenRouter.ai. It supports model switching, logs latency and token counts, and persists logs in a CSV file.

## Features
- Route prompts to **Mistral-7B** or **Llama-3.1-8B Instruct** using a model parameter
- Log round-trip latency, token counts, model used and timestamp for each prompt/response
- Persist logs in a CSV file (`chat_logs.csv`)
- Simple HTTP API (`POST /chat`)
- Health check endpoint (`GET /health`)
- Simple automated tests

## Requirements
- Python 3.8+
- OpenRouter.ai API key (free to obtain)

## Setup
1. **Clone the repo**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**
   - Create a `.env` file in the project root:
     ```
     OPENROUTER_API_KEY=your_openrouter_api_key_here
     ```
   - Get your key from [https://openrouter.ai/](https://openrouter.ai/)

## Running the Service
```bash
uvicorn main:app --reload
```
- The API will be available at `http://127.0.0.1:8000`

## API Usage
### Health Check
```http
GET /health
```
- Returns `{ "status": "ok" }`

### Chat Endpoint
```http
POST /chat
Content-Type: application/json
{
  "prompt": "Your question here",
  "model": "mistral" | "llama"
}
```
- `model` must be `mistral` or `llama`.
- Returns: model response, latency, token counts, model used and timestamp in JSON.

## Logging
- All interactions are logged to `chat_logs.csv` with:
  - Timestamp
  - Model
  - Prompt
  - Response
  - Latency
  - Prompt tokens
  - Response tokens

## Testing
```bash
pytest
```
- Runs simple tests for the health and chat endpoints.

## For Evaluator

- **Public API URL:** [https://promptcue-llm-chat-api.onrender.com/](https://promptcue-llm-chat-api.onrender.com/)  
- **Supported models:** "mistral" and "llama"
- **How to test:**

  - Use the interactive Swagger UI at `/docs`:
  [https://promptcue-llm-chat-api.onrender.com/docs/](https://promptcue-llm-chat-api.onrender.com/docs/)
  
  - Use the `/chat` endpoint with a POST request. The `model` field must be either `"mistral"` or `"llama"` (not both):
  ```json
  {
    "prompt": "Hello, who are you?",
    "model": "mistral"
  }
  ```


  ### Testing with Postman

  - Open Postman and create a new `POST` request.
  - Set the request URL to your deployed API, e.g.:
     ```
     https://promptcue-llm-chat-api.onrender.com/chat
     ```
  - Go to the "Body" tab, select "raw" and choose "JSON" as the format.
  - Enter the following JSON (choose either model):
     ```json
     {
       "prompt": "Hello, who are you?",
       "model": "mistral"
     }
     ```
  - Click "Send".
  - You should receive a JSON response with the model's reply, latency, token counts, etc.

  You can also use the `/docs` endpoint in your browser for interactive API testing.
- **No local setup required.**
- **Logs:** All interactions are logged to `chat_logs.csv` (available in the repo after running a few prompts).


## Example Log Analysis

The `chat_logs.csv` file records every interaction with the chat service, capturing key metrics for both supported models (`mistral` and `llama`).


### Sample Log Entries

| timestamp                  | model    | prompt                                                      | latency (s) | prompt_tokens | response_tokens |
|----------------------------|----------|-------------------------------------------------------------|-------------|---------------|-----------------|
| 2025-07-15T17:20:47.475859 | mistral  | Hello, who are you?                                         | 3.97        | 4             | 47              |
| 2025-07-15T17:25:03.890301 | llama    | How can LLMs model benefits a Tech Startup                  | 13.79       | 8             | 446             |
| 2025-07-15T17:28:11.275427 | llama    | Tell in three points how you and mistral LLM is different?  | 17.32       | 11            | 258             |

### What This Demonstrates

- **Model Switching:** Prompts are routed to both `mistral` and `llama`, confirming multi-model support.
- **Latency Tracking:** Each entry logs the time taken for the model to respond.
- **Token Counts:** Both prompt and response token counts are recorded, showing the system’s ability to track usage.
- **Prompt Variety:** The log demonstrates the system’s versatility with a range of prompt types.

## Deployment Note

This project is hosted on Render's free tier.  
To conserve resources, Render puts the server to sleep after 15 minutes of inactivity.  
As a result, the **first request may take 30–60 seconds** while the server "spins up" (cold start).  
Subsequent requests will respond quickly.

If you experience a delay, please wait a moment — the server is waking up.  
Thank you for your patience!
