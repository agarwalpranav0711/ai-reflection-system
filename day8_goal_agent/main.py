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


# 🔹 STEP 1: PLAN
def create_plan(goal):
    prompt = f"""
You are an AI planner.

Break this goal into steps:

Goal:
{goal}

Return steps as a numbered list.
"""
    return call_llm(prompt)


# 🔹 STEP 2: EXECUTE
def execute_plan(plan):
    prompt = f"""
Execute the following plan step by step:

{plan}

Give final result.
"""
    return call_llm(prompt)


# 🔹 MAIN SYSTEM
def run_agent(goal):
    print("\n🧠 GOAL:\n", goal)

    plan = create_plan(goal)
    print("\n📋 PLAN:\n", plan)

    result = execute_plan(plan)
    print("\n✅ RESULT:\n", result)

    return result


# 🔹 TEST
if __name__ == "__main__":
    run_agent("Explain latest AI trends in simple terms")