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


# 🔁 AGENT LOOP
def run_agent(goal):
    print("\n🎯 Goal:", goal)

    observation = ""

    for step in range(5):  # give more steps
        print(f"\n🔁 Step {step+1}")

        prompt = f"""
You are an AI agent.

Goal:
{goal}

Previous observation:
{observation}

Decide the NEXT step.

Rules:
- Break the goal into steps
- If the goal is COMPLETELY achieved, say DONE: yes
- Otherwise say DONE: no
- Do NOT repeat steps
- Stop after final result is ready

Return format:
PLAN: ...
ACTION: ...
DONE: yes/no
"""

        output = call_llm(prompt)
        print("🧠 LLM OUTPUT:\n", output)

        # update observation
        observation = f"{observation}\n{output}"

        # stop condition
        if "done: yes" in output.lower():
            print("\n✅ Goal Completed!")
            break

    print("\n🏁 Final Observation:\n", observation)


# 🧪 TEST
if __name__ == "__main__":
    goal = input("Enter your goal: ")
    run_agent(goal)