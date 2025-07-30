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
        self.center_storage.append(item)

    def get_center_storage_string(self):
        items = self.center_storage
        total = len(items)
        if total == 0:
            return "Storage is empty."

        # Count items manually
        counts = {}
        for item in items:
            if item not in counts:
                counts[item] = 0
            counts[item] += 1

        # Build summary
        summary_parts = []
        for item, count in counts.items():
            percentage = (count / total) * 100
            summary_parts.append(f"{item}: {count} ({percentage:.1f}%)")

        return ", ".join(summary_parts)
    
    def get_id_by_name(self, name):
        """Find task ID by its Name (case-insensitive)."""
        for task in self.tasks:
            if task.get("Name").lower() == name.lower():
                return task.get("ID")
        return None

        