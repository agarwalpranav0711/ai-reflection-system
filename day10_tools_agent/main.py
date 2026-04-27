import requests
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


# 🔹 LLM CALL
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


# 🔹 TOOL 1: CALCULATOR
def calculator_tool(expression):
    try:
        return str(eval(expression))
    except:
        return "Calculation error"


# 🔹 TOOL 2: SEARCH (MOCK)


SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_tool(query):
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "organic_results" in results:
            top_results = results["organic_results"][:3]

            output = ""
            for r in top_results:
                output += f"{r.get('title')} - {r.get('snippet')}\n"

            return output

        return "No results found"

    except Exception as e:
        return f"Search error: {e}"


# 🔹 TOOL EXECUTOR
def execute_tool(action):
    action = action.replace("ACTION:", "").strip()

    if action.lower().startswith("calculator"):
        expr = action.split(":", 1)[-1].strip()
        return calculator_tool(expr)

    elif action.lower().startswith("search"):
        query = action.split(":", 1)[-1].strip()
        return search_tool(query)

    else:
        return "No valid tool used"


# 🔁 AGENT LOOP
def run_agent(goal):
    print("\n🎯 Goal:", goal)

    observation = ""

    for step in range(5):
        print(f"\n🔁 Step {step+1}")

        prompt = f"""
You are an AI agent with tools.

Tools:
1. calculator → for math
2. search → for real-world info

Rules:
- Use calculator ONLY for numbers
- Use search for facts, news, info
- Always choose correct tool
- Stop when goal is completed

Goal:
{goal}

Previous observation:
{observation}

Return:
PLAN: ...
ACTION: tool_name: input
DONE: yes/no
"""

        output = call_llm(prompt)
        print("🧠 LLM OUTPUT:\n", output)

        # 🔥 Extract ACTION
        action_line = [line for line in output.split("\n") if "ACTION" in line]
        action = action_line[0] if action_line else ""

        result = execute_tool(action)

        print("⚙️ TOOL RESULT:", result)
        

        # 🔥 update observation properly
        observation = f"{observation}\nAction: {action}\nResult: {result}"

        if "done: yes" in output.lower():
            print("\n✅ Goal Completed!")
            break

    print("\n🏁 Final Observation:\n", observation)

# 🧪 TEST
if __name__ == "__main__":
    goal = input("Enter your goal: ")
    run_agent(goal)