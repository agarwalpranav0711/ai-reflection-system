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


# 🔥 Confidence system
def confidence_prompt(question):
    return f"""
Answer the question and ALSO give:

- confidence (0 to 100)
- reason

Return ONLY JSON in this format:

{{
  "answer": "...",
  "confidence": number,
  "reason": "..."
}}

Question:
{question}
"""


def run_system(question):
    output = call_llm(confidence_prompt(question))

    print("\nRAW OUTPUT:\n", output)

    # clean markdown if present
    output = output.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(output)
        return parsed
    except:
        print("❌ JSON parsing failed")
        return {"error": output}


# 🧪 Test
if __name__ == "__main__":
    result = run_system("Explain machine learning simply")

    print("\n--- FINAL OUTPUT ---\n")
    print(result)

    if "confidence" in result:
        print(f"\nConfidence: {result['confidence']}%")

        if result["confidence"] < 70:
            print("⚠️ Low confidence — needs improvement")
        else:
            print("✅ Good confidence")