import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

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


# 🔹 Build prompt with memory
def build_prompt(question, memory):
    past = ""

    # include last 3 interactions
    for item in memory[-3:]:
        past += f"Q: {item['question']}\nA: {item['answer']}\n\n"

    return f"""
You are a helpful AI.

Here is past conversation:
{past}

Now answer the new question:

{question}
"""


# 🔹 Main system
def run_system(question):
    memory = load_memory()

    prompt = build_prompt(question, memory)

    answer = call_llm(prompt)

    print("\nANSWER:\n", answer)

    # store new interaction
    memory.append({
        "question": question,
        "answer": answer
    })

    save_memory(memory)


# 🧪 Test loop
if __name__ == "__main__":
    while True:
        q = input("\nAsk something: ")
        if q.lower() == "exit":
            break

        run_system(q)