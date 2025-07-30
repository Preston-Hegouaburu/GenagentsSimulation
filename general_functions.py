import requests
import json
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

def replace_inputs_in_txt(file_path, *inputs):
    # Read the contents of the .txt file
    with open(file_path, 'r') as file:
        content = file.read()

    # Loop through each input and replace its placeholder
    for i, value in enumerate(inputs, start=1):
        placeholder = f'|INPUT{i}|'
        content = content.replace(placeholder, str(value))

    return content




