from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

# 🔹 LLM FUNCTION
def llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]


# 🔹 STEP 1: GENERATE
def generate_answer(question):
    return llm(f"Answer this clearly:\n{question}")


# 🔹 STEP 2: REVIEW
def review_answer(answer):
    prompt = f"""
You are a strict reviewer.

Check:
- correctness
- missing info
- clarity

Give:
1. Problems
2. Suggestions
3. Score out of 10

Answer:
{answer}
"""
    return llm(prompt)


# 🔹 STEP 3: IMPROVE
def improve_answer(answer, review):
    prompt = f"""
Improve the answer using feedback.

Original:
{answer}

Feedback:
{review}

Fix everything and make it better.
"""
    return llm(prompt)


# 🔹 PIPELINE
def reflection_pipeline(question):
    answer = generate_answer(question)
    review = review_answer(answer)
    improved = improve_answer(answer, review)

    return {
        "answer": answer,
        "review": review,
        "improved_answer": improved
    }


# 🔹 API
@app.get("/ask")
def ask(question: str):
    return reflection_pipeline(question)