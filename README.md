# primeAPI

FastAPI + OpenAI + Oracle REST API.

## Local Setup

1. Create a `.env` file (copy from `.env.example`):
   ```
   OPENAI_API_KEY=your_key
   ORACLE_USER=your_user
   ORACLE_PASSWORD=your_password
   ORACLE_DSN=host:port/servicename
   ```

2. Install and run:
   ```bash
   pip install -r requirements.txt
   uvicorn openai_rest:app --reload
   ```

3. POST to `/ask` with `{"question": "your question"}`
