from fastapi import FastAPI
import requests
import os
import json
from dotenv import load_dotenv

# 🔹 Load API Key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

MEMORY_FILE = "memory.json"


# 🔹 Load memory
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# 🔹 Save memory
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# 🔹 LLM call
def call_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data, timeout=20)
    return response.json()["choices"][0]["message"]["content"]


# 🔹 ASK ENDPOINT
@app.post("/ask")
def ask_ai(question: str):
    memory = load_memory()

    # 🔥 ADD MEMORY INTO PROMPT
    memory_text = "\n".join(
        [f"Q: {m['question']} A: {m['answer']}" for m in memory[-5:]]
    )

    prompt = f"""
You are a smart AI with memory.

Here is past conversation:
{memory_text}

Rules:
- If unsure, say "I don't know"
- Do NOT guess
- Return ONLY JSON

Format:
{{
 "answer": "...",
 "confidence": number
}}

Question:
{question}
"""

    output = call_llm(prompt)

    # 🔥 SAFE JSON EXTRACTION
    start = output.find("{")
    end = output.rfind("}") + 1

    if start == -1 or end == -1:
        return {
            "final_answer": "I don't know",
            "confidence": 0
        }

    clean_output = output[start:end]

    try:
        parsed = json.loads(clean_output)
    except:
        return {
            "final_answer": "I don't know",
            "confidence": 0
        }

    # 🔥 CONFIDENCE FIX
    confidence = parsed.get("confidence", 0)

    if confidence <= 1:  # convert 0.9 → 90
        confidence *= 100

    # 🔥 SAFETY CHECK
    if confidence < 60:
        final = "I don't know"
    else:
        final = parsed.get("answer", "I don't know")

    # 🔥 SAVE MEMORY
    memory.append({
        "question": question,
        "answer": final
    })
    save_memory(memory)

    return {
        "final_answer": final,
        "confidence": confidence
    }


# 🔹 HISTORY ENDPOINT
@app.get("/history")
def get_history():
    return load_memory()


# 🔹 IMPROVE ENDPOINT
@app.post("/improve")
def improve_answer(text: str):

    prompt = f"""
Improve this answer:

{text}
"""

    improved = call_llm(prompt)

    return {"improved": improved}