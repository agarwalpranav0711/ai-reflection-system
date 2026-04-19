import requests
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda

# 🔐 Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

print("API KEY LOADED:", API_KEY is not None)  # debug check


# 🔹 LLM FUNCTION (FIXED)
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

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=20   # 🔥 prevents hanging
        )

        print("Status Code:", response.status_code)

        res = response.json()

        if "choices" not in res:
            print("API ERROR:", res)
            return "Error: Invalid API response"

        return res["choices"][0]["message"]["content"]

    except Exception as e:
        print("Request failed:", e)
        return "Error: Request failed"


llm = RunnableLambda(call_llm)


# ✍️ WRITER
def writer_prompt(question):
    return f"""
You are a helpful AI writer.

Write a clear and detailed answer.

Question:
{question}
"""

writer_chain = RunnableLambda(writer_prompt) | llm


# 🧠 CRITIC
def critic_prompt(answer):
    return f"""
You are a strict critic.

Analyze this answer and give:
- Problems
- Missing points
- Suggestions

Answer:
{answer}
"""

critic_chain = RunnableLambda(critic_prompt) | llm


# 🔁 IMPROVER
def improve_prompt(data):
    answer = data["answer"]
    review = data["review"]

    return f"""
Improve the answer using this feedback.

Original Answer:
{answer}

Feedback:
{review}

Fix all issues and make it better.
"""

improve_chain = RunnableLambda(improve_prompt) | llm


# 🔗 SYSTEM
def run_system(question):
    logs = {}

    print("\n⚡ Running Writer...\n")
    answer = writer_chain.invoke(question)
    logs["initial_answer"] = answer

    print("\n🧠 Running Critic...\n")
    review = critic_chain.invoke(answer)
    logs["review"] = review

    print("\n🔁 Improving Answer...\n")
    improved = improve_chain.invoke({
        "answer": answer,
        "review": review
    })
    logs["improved_answer"] = improved

    return logs


# 🧪 TEST
if __name__ == "__main__":
    result = run_system("Explain machine learning simply")

    print("\n--- INITIAL ANSWER ---\n")
    print(result["initial_answer"])

    print("\n--- REVIEW ---\n")
    print(result["review"])

    print("\n--- IMPROVED ANSWER ---\n")
    print(result["improved_answer"])