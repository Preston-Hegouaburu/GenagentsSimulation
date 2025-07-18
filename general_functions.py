import requests
import json
import os
from agent import Agent

def ask(prompt: str):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 'your key here'",
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

def replace_inputs_in_txt(file_path, input1, input2, input3, input4):
    # Read the contents of the .txt file
    with open(file_path, 'r') as file:
        content = file.read()

    # Perform replacements
    replacements = {
        '|INPUT1|': input1,
        '|INPUT2|': input2,
        '|INPUT3|': input3,
        '|INPUT4|': input4
    }

    for key, value in replacements.items():
        content = content.replace(key, value)

    return content

def load_all_agents(base_dir='agents'):
    agents = []
    for name in os.listdir(base_dir):
        agent_path = os.path.join(base_dir, name)
        print(name)
        if os.path.isdir(agent_path):
            agents.append(Agent(name, base_dir))
    return agents



