import os
import json
import time

# Define this globally or pass it in from outside the class
SIMULATION_START_TIME = time.time()

class Agent:
    def __init__(self, name, base_dir='agents'):
        self.name = name
        self.agent_dir = os.path.join(base_dir, name)
        self.memory_path = os.path.join(self.agent_dir, 'memory.json')
        self.memory_path = os.path.join(self.agent_dir, 'background.json')
        self.config_path = os.path.join(self.agent_dir, 'config.json')

    def load_memory(self):
        return self._load_json(self.memory_path)

    def load_config(self):
        return self._load_json(self.config_path)
    
    def get_background(self):
        return 
    
    def save_memory(self, data):
        print(f"[DEBUG] Writing to {self.memory_path}")
        with open(self.memory_path, 'w') as f:
            json.dump(data, f, indent=2)

    def save_config(self, data):
        self._save_json(self.config_path, data)

    def add_memory_entry(self, text, memory_type, sim_step):
        memory_entry = {
            "type": memory_type,
            "text": text,
            "simulationstep": sim_step,
            "importance": 0
        }

        try:
            memory_data = self.load_memory()
        except (FileNotFoundError, json.JSONDecodeError):
            print("oh no")
            memory_data = []

        memory_data.append(memory_entry)
        self.save_memory(memory_data)

        print(f"Saved memory to {self.name}/memory.json: {memory_entry}")

    def _load_json(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def _save_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
