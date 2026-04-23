import requests
import os
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


# 🔹 Normal answer
def normal_prompt(question):
    return f"Answer this question:\n{question}"


# 🔹 Step-by-step reasoning
def reasoning_prompt(question):
    return f"""
Solve this step-by-step.

Explain your reasoning clearly.
Then give the final answer.

Question:
{question}
"""


def run_system(question):
    print("\n⚡ NORMAL ANSWER:\n")
    normal = call_llm(normal_prompt(question))
    print(normal)

    print("\n🧠 STEP-BY-STEP ANSWER:\n")
    reasoning = call_llm(reasoning_prompt(question))
    print(reasoning)


if __name__ == "__main__":
    run_system("If a train travels 60 km in 1 hour, how far in 3 hours?")