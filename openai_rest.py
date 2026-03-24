from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import oracledb
import json
import os

app = FastAPI()
#path = "INV.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QuestionRequest(BaseModel):
    question: str


def read_oracle(query):
    connection = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN"),
    )

    cursor = connection.cursor()
    cursor.execute(query)

    columns = [col[0].lower() for col in cursor.description]

    result = []
    for row in cursor:
        clean_row = {}
        for col, val in zip(columns, row):
            if hasattr(val, "isoformat"):
                clean_row[col] = val.isoformat()
            else:
                clean_row[col] = val
        result.append(clean_row)

    cursor.close()
    connection.close()

    return json.dumps(result, indent=2, default=str)
    #return json.dumps(result, indent=2)


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return json.dumps(data, indent=2)




@app.post("/ask")
def ask_question(request: QuestionRequest):
    # ⚠️ Keep query SMALL (important)
    query = "SELECT * FROM hai_sales" #FETCH FIRST 50 ROWS ONLY"
    document_text = read_oracle(query)

    #document_text = read_json(path)

    conversation = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Use ONLY the provided data. "
                #"Do NOT perform calculations. "
                "If answer not found, say 'I don't know.'\n\n"
                f"DATA:\n{document_text}"
            )
        },
        {
            "role": "user",
            "content": request.question
        }
    ]

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=conversation
    )

    return {
        "answer": response.output_text
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))