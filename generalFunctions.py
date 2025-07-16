import requests
import json
import time
import os

def ask(prompt: str):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
            ##"HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            ##"X-Title": "<YOUR_SITE_NAME>",      # Optional
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "tngtech/deepseek-r1t2-chimera:free", 
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
    )

    # Parse and print the response content
    if response.status_code == 200:
        result = response.json()
        print("yay")
        return result["choices"][0]["message"]["content"]
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

SIMULATION_START_TIME = time.time()

def save_memory_entry(text, memory_type, agent_index):
    agents_folder = "agents"

    # Get agent folder names
    agent_names = sorted(
        [name for name in os.listdir(agents_folder) if os.path.isdir(os.path.join(agents_folder, name))]
    )

    if agent_index < 0 or agent_index >= len(agent_names):
        raise IndexError("Invalid agent index")

    agent_name = agent_names[agent_index]
    memory_path = os.path.join(agents_folder, agent_name, "memory.json")

    # Calculate time since program started
    elapsed_time = round(time.time() - SIMULATION_START_TIME, 2)

    memory_entry = {
        "type": memory_type,
        "text": text,
        "timestamp": elapsed_time,
        "importance": 0
    }

    # Load and update memory.json
    if os.path.exists(memory_path):
        with open(memory_path, "r") as f:
            try:
                memory_data = json.load(f)
            except json.JSONDecodeError:
                memory_data = []
    else:
        memory_data = []

    memory_data.append(memory_entry)

    with open(memory_path, "w") as f:
        json.dump(memory_data, f, indent=2)

    print(f"Saved memory to {agent_name}/memory.json: {memory_entry}")

