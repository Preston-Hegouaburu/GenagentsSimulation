import os
import json

class Tasks:
    def __init__(self):
        self.center_storage = []
        # Load the JSON data from a file
        with open('tasks.json', 'r') as f:
            self.tasks = json.load(f)
    
    def get_task_by_id(self, task_id):
        """Return the task dictionary that matches the given task ID."""
        for task in self.tasks:
            if task.get("ID") == task_id:
                return task
        return None

    def get_name(self, task_id):
        """Return the Name of the task with the given ID."""
        task = self.get_task_by_id(task_id)
        return task.get("Name") if task else None

    def get_gives(self, task_id):
        """Return what the task gives."""
        task = self.get_task_by_id(task_id)
        return task.get("Gives") if task else None

    def get_type(self, task_id):
        """Return the type of the task."""
        task = self.get_task_by_id(task_id)
        return task.get("type") if task else None
    
    def add_item_to_storage(self, item):
        print(self.center_storage)
        self.center_storage.append(item)

    def get_num_items_in_center_storage(self):
        print(self.center_storage)
        if len(self.center_storage) == 0:
            return ""
        return str(len(self.center_storage)) + " Items in Storage. Storage cannot be empty"

    def get_center_storage_string(self):
        print(self.center_storage)
        from collections import Counter
        items = self.center_storage
        

        resource_types = ["Metal", "Wood", "Water", "Food"]
        total = len(items)
        count = Counter(items)

        if total == 0:
            return "Storage is currently empty."

        parts = []
        for resource in resource_types:
            percentage = (count[resource] / total) * 100 if total > 0 else 0
            parts.append(f"{resource}: {round(percentage, 1)}%")
        
        return " ".join(parts)
    
    def get_id_by_name(self, name):
        """Find task ID by its Name (case-insensitive)."""
        for task in self.tasks:
            if task.get("Name").lower() == name.lower():
                return task.get("ID")
        return None

        