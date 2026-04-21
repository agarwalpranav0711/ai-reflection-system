import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


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


# 🔥 Hallucination-safe prompt
def safe_prompt(question):
    return f"""
You are a truthful and careful AI.

Rules:
- If you are unsure, say "I don't know"
- Do NOT guess
- Do NOT make up facts

You MUST:
- Give confidence as an INTEGER between 0 and 100
- DO NOT use decimals (❌ 0.8, 1.0)
- ONLY use whole numbers (✅ 25, 70, 95)

Return ONLY valid JSON (no extra text):

{{
  "answer": "...",
  "confidence": 85,
  "reason": "..."
}}

Question:
{question}
"""

def run_system(question):
    output = call_llm(safe_prompt(question))

    print("\nRAW OUTPUT:\n", output)

    output = output.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(output)
    except:
        return {"error": output}

    # 🔥 CONTROL LOGIC
    if parsed["confidence"] < 60:
        parsed["final_answer"] = "I don't know"
    else:
        parsed["final_answer"] = parsed["answer"]

    return parsed


# 🧪 TEST
if __name__ == "__main__":
    result = run_system("What is machine learning?")
    # result = run_system("Who is the king of Mars?")

    print("\n--- FINAL OUTPUT ---\n")
    print(result)