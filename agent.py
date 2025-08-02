import os
import json
import re, json
import time
import general_functions
import scentence_similarity
from pathfinding import a_star
from sim_step_manager import SimulationStep
# Define this globally or pass it in from outside the class

class Agent:
    def __init__(self, name, x, y, sim_step_manager, base_dir='agents'):
        self.name = name
        self.x = x
        self.y = y
        self.record_path = os.path.join(base_dir, 'record.txt')
        self.agent_dir = os.path.join(base_dir, name)
        self.memory_path = os.path.join(self.agent_dir, 'memory.json')
        self.background_path = os.path.join(self.agent_dir, 'background.json')
        self.config_path = os.path.join(self.agent_dir, 'config.json')
        self.situation = ""
        self.holding = "None"
        if self.load_memory() == []:
            self.set_up_personality(sim_step_manager)
        
        self.importance_threshold = 75
        self.importance_trigger = self.importance_threshold
        self.num_memories_to_reflect = 0
        self.retention = 5
        self.total_communications = 0
        self.total_moves = 0
    
    def write_to_records(self, text):
        with open(self.record_path, "a") as file:
            file.write(text + "\n")

    def load_memory(self):
        return self._load_json(self.memory_path)

    def load_config(self):
        return self._load_json(self.config_path)
    
    def get_background(self):
        return 
    
    def save_memory(self, data):
        with open(self.memory_path, 'w') as f:
            json.dump(data, f, indent=2)

    def save_config(self, data):
        self._save_json(self.config_path, data)

    def _load_json(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def _save_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def add_memory_entry(self, text, memory_type, sim_step_manager):
        memory_entry = {
            "type": memory_type,
            "text": text,
            "simulationstep": sim_step_manager.get_sim_step(),
            "importance": 0
        }

        try:
            memory_data = self.load_memory()
        except (FileNotFoundError, json.JSONDecodeError):
            print("oh no")
            memory_data = []

        memory_data.append(memory_entry)
        self.save_memory(memory_data)

        #print(f"Saved memory to {self.name}/memory.json: {memory_entry}")

    def describe_self(self, text):
            self_describe_path = os.path.join("templates", "memory_evaluation", "self_describe.txt")
            return general_functions.ask(general_functions.replace_inputs_in_txt(self_describe_path, self.name, text))
    
    def communication_to_text(self, communications, sim_step_manager):
        result = ""
        for line in communications:
            self.add_memory_entry(result, "communicaiton", sim_step_manager)
            if f"[{self.name}]" not in line and line != "":
                result += line + "\n"
        return result

    def get_spatial_memories_as_string(self):
        """
        Reads a JSON file of memories and returns a single string
        containing all 'spatial observation' memory texts, separated by spaces.
        """
        try:
            with open(self.memory_path, "r") as f:
                memories = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error reading JSON file: {e}")
        
        # Filter only "spatial observation" memories
        spatial_memories = [
            memory["text"].strip()
            for memory in memories
            if memory.get("type") == "spatial observation"
        ]

        # Join them into one long string
        return " ".join(spatial_memories)


    def reflect(self, sim_step_manager):
        if self.importance_trigger <= 0:
            reasoning_path = os.path.join("templates", "memory_evaluation", "reflect.txt")
            self.importance_trigger = self.importance_threshold
            self.refelctions_to_memories(general_functions.ask(general_functions.replace_inputs_in_txt(reasoning_path, self.name, self.get_recent_memories(self.num_memories_to_reflect))), sim_step_manager)
            self.num_memories_to_reflect = 0


    def refelctions_to_memories(self, insight_str, sim_step_manager):

        insight_str = insight_str.strip()
        if insight_str.startswith("```json"):
            insight_str = re.sub(r"^```json\s*", "", insight_str)
            insight_str = re.sub(r"\s*```$", "", insight_str)
        
        try:
            data = json.loads(insight_str)
        except json.JSONDecodeError as e:
            print("reflection did not work")
            return

        # Extract insights list
        insights = data.get("insights", [])
        


        if not isinstance(insights, list):
            raise ValueError("'insights' is not a list in the provided JSON string.")
        for item in insights:
            self.add_memory_entry(item, "reflection", sim_step_manager)

    def get_recent_memories(self, num_memories):
        with open(self.memory_path, 'r') as f:
            memories = json.load(f)

        result = ""

        for i in range(num_memories):
            result += memories[i].get("text", "") + "\n"

        return result.strip()

    def communicate_or_move(self, world, sim_step_manager):
        communications = self.communication_to_text(sim_step_manager.get_communications(), sim_step_manager)
        communicate_or_move_path = os.path.join("templates", "interaction", "move_or_communicate.txt")
        communicate_or_move_path_respond = os.path.join("templates", "interaction", "move_or_communicate_respond.txt")
        if communications != "":
            answer = general_functions.ask(general_functions.replace_inputs_in_txt(communicate_or_move_path_respond, scentence_similarity.retrieve_top_memories(self.memory_path, self.situation, sim_step_manager.get_sim_step()), self.situation, communications))
        else:
            answer = general_functions.ask(general_functions.replace_inputs_in_txt(communicate_or_move_path, scentence_similarity.retrieve_top_memories(self.memory_path, self.situation, sim_step_manager.get_sim_step()), self.situation))
            print("In deciding to move or communicate I " + self.name +" have decided: " + answer)
            self.write_to_records("In deciding to move or communicate I " + self.name +" have decided: " + answer)
        if "no" not in answer:
            print("communicating")
            self.total_communications += 1
            self.write_to_records(self.name + " Communicating")
            self.write_to_records(self.name + "Total communications: " + str(self.total_communications) + ", Total moves: " + str(self.total_moves))
            self.determine_communication(sim_step_manager, answer)
        else:
            print("Moving")
            self.total_moves += 1
            self.write_to_records(self.name + " Moving")
            self.write_to_records(self.name + "Total communications: " + str(self.total_communications) + ", Total moves: " + str(self.total_moves))
            self.determine_move(world, sim_step_manager)

    def determine_communication(self, sim_step_manager, communicatiee):
        communicate_path = os.path.join("templates", "interaction", "communicate_outwards.txt")
        communication = general_functions.ask(general_functions.replace_inputs_in_txt(communicate_path, self.name, self.situation, scentence_similarity.retrieve_top_memories(self.memory_path, self.situation, sim_step_manager.get_sim_step()), communicatiee))
        print("my communication: " + communication)
        self.write_to_records(self.name + " communication is: " + communication)
        sim_step_manager.add_communications(self.name, communication)
    
    def determine_move(self, world, sim_step_manager):
        move_path_object = os.path.join("templates", "interaction", "move_object.txt")
        position_str = general_functions.ask(general_functions.replace_inputs_in_txt(move_path_object, self.name, self.situation, self.get_spatial_memories_as_string, scentence_similarity.retrieve_top_memories(self.memory_path, self.situation, sim_step_manager.get_sim_step())))
        print(self.name + "'s movement string: "+position_str)
        self.write_to_records(self.name + "'s movement string: "+position_str)
        if "no" in position_str:
            print("I have decided to move areas")
            self.write_to_records(self.name + "has decided to move to another area")
            self.move_area(world, sim_step_manager)
            return
        try:
            position = json.loads(position_str)  # This gives [2, 3] as a Python list of ints
        except:
            return
        self.move(position[0],position[1],world)
    
    def move_area(self, world, sim_step_manager):
        move_path_object = os.path.join("templates", "interaction", "move_area.txt")
        position_str = general_functions.ask(general_functions.replace_inputs_in_txt(move_path_object, self.name, self.situation, self.get_spatial_memories_as_string, scentence_similarity.retrieve_top_memories(self.memory_path, self.situation, sim_step_manager.get_sim_step())))
        position_str = position_str.lower()
        self.write_to_records(self.name + "has decided to move to area: " + position_str)
        if "upper left" in position_str:
            self.move(4, 4, world)
        elif "upper right" in position_str:
            self.move(14, 4, world)
        elif "lower right" in position_str:
            self.move(14, 14, world)
        elif "lower left" in position_str:
            self.move(4, 14, world)
        elif "storage" in position_str:
            self.move(9, 9, world)
        

    def interact(self, num, sim_step_manager, task_system):
        if num == 5:
            if task_system.get_num_items_in_center_storage() == "":
                self.add_memory_entry("No items in storage currently", "observation", sim_step_manager)
            else:
                self.add_memory_entry(task_system.get_num_items_in_center_storage(), "observation", sim_step_manager)
                self.add_memory_entry("Center storage recource percentages: " + task_system.get_center_storage_string(), "observation", sim_step_manager)
            interaction_str = os.path.join("templates", "interaction", "interact_with_task_storage.txt")
            if self.holding != "None":
                response = general_functions.ask(general_functions.replace_inputs_in_txt(interaction_str, self.name, self.situation, scentence_similarity.retrieve_top_memories(self.memory_path, self.situation, sim_step_manager.get_sim_step()), self.holding))
                if "yes" in response:
                    task_system.add_item_to_storage(self.holding)
                    self.holding = "None"
        else:
            interaction_str = os.path.join("templates", "interaction", "interact_with_task_getter.txt")
            response = general_functions.ask(general_functions.replace_inputs_in_txt(interaction_str, self.name, self.situation, scentence_similarity.retrieve_top_memories(self.memory_path, self.situation, sim_step_manager.get_sim_step()), self.holding, task_system.get_name(num), task_system.get_gives(num)))
            if "yes" in response:
                self.holding = task_system.get_gives(num)

    def zero_importace_memories_to_text(self):
   
        with open(self.memory_path, 'r') as f:
            memories = json.load(f)

        result = ""

        for memory in memories:
            if memory.get("importance", 0) == 0:
                result += memory.get("text", "") + "\n"
        print(result.strip())
        return result.strip()  # Remove extra newline at the end

    def evaluate_importance(self):
        importance_path = os.path.join("templates", "memory_evaluation", "importance.txt")
        if self.zero_importace_memories_to_text() != "":
            #The llm is prompted with the importance.txt template with the memories, given by the funciton zero_importance... then the llm response is passed into update_importance_scores
            self.update_importance_scores(general_functions.ask(general_functions.replace_inputs_in_txt(importance_path, self.zero_importace_memories_to_text())))
        
    def update_importance_scores(self, llm_response):

        # Step 1: Parse the LLM response
        print(llm_response)
        try:
            scores = json.loads(llm_response)
            print(scores)
        except json.JSONDecodeError:
            match = re.search(r"\[.*?\]", llm_response, re.DOTALL)
            if not match:
                raise ValueError("Could not parse importance scores from LLM response.")
            scores = json.loads(match.group(0))

        if not isinstance(scores, list) or not all(isinstance(s, int) for s in scores):
            raise ValueError("Parsed importance scores are not a valid list of integers.")

        # Step 2: Load the current memories
       
        memories = self._load_json(self.memory_path)

        if len(memories) == 0:
            raise ValueError("Memory file is empty.")

        # Step 3: Assign scores to the most recent entries
        num_scores = len(scores)
        if num_scores > len(memories):
            raise ValueError("More scores provided than total memories in the file.")

        # Find the target slice (most recent entries)
        start_index = len(memories) - num_scores
        for memory, score in zip(memories[start_index:], scores):
            self.importance_trigger -= score
            if self.num_memories_to_reflect < 25:
                self.num_memories_to_reflect += 1
            memory["importance"] = score

        # Step 4: Save updated memories
        with open(self.memory_path, "w") as f:
            json.dump(memories, f, indent=2)

    def set_up_personality(self, sim_step_manager):
        before, personality, beliefs = self.split_agent_data()
        self.add_memory_entry(self.describe_self(before), "observation", sim_step_manager)
        self.add_memory_entry(self.describe_self(personality), "observation", sim_step_manager)
        self.add_memory_entry(self.describe_self(beliefs), "observation", sim_step_manager)

    def split_agent_data(self):
        data = self._load_json(self.background_path)

        before_personality = []
        personality_parts = []
        beliefs_parts = []

        # Loop through top-level keys
        for key, value in data.items():
            if key == "personality":
                # Flatten personality traits, likes, dislikes
                for p_key, p_value in value.items():
                    personality_parts.append(f"{p_key}: {', '.join(p_value)}")
            elif key == "beliefs":
                # Flatten beliefs into one string
                beliefs_parts.append("beliefs: " + "; ".join(value))
            else:
                # Add to the 'before_personality' string
                before_personality.append(f"{key}: {value}")

        # Join all parts into stringstion module generated text observatio
        before_personality_str = " ".join(before_personality)
        personality_str = " ".join(personality_parts)
        beliefs_str = " ".join(beliefs_parts)

        return before_personality_str, personality_str, beliefs_str

    
    def memory_contains_text(self, search_text):
        """
        Returns True if the search_text is found in any memory's text field.
        """
        search_text = search_text.lower().strip()

        memories = self._load_json(self.memory_path)

        for memory in memories:
            if search_text in memory.get("text", "").lower():
                return True
        return False


    def move(self, dx, dy, world):
        nx, ny = dx, dy
        if world.is_walkable(nx, ny):
            world.remove_event_from_tile(self.x, self.y, self.name)
            self.x, self.y = nx, ny
            world.add_event_to_tile(self.x, self.y, self.name)
            return True
        return False

    def observe_surroundings(self, world, sim_step_manager, task_system, radius=3):
        """Observe events nearby and log them to memory."""
        descriptions = []
        saw_interactable = False
        num = 0
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < world.width and 0 <= ny < world.height:
                    for event in world.memory_grid[ny][nx].events:
                        if event != None:
                            if ("Task" in event):
                                num = int(event.split()[-1])  # Take the last part of the string and convert to int
                                spatial_observation = f"{task_system.get_name(num)} is at ({nx},{ny})."
                                observation = f"{self.name} saw {task_system.get_name(num)}."
                                saw_interactable = True
                            else:
                                spatial_observation = f"{event} is at ({nx},{ny})."
                                observation = f"{self.name} saw {event} in {world.area_grid[self.x][self.y]}."
                            descriptions.append(observation)
                            self.add_memory_entry(observation, "observation", sim_step_manager)
                            if not self.memory_contains_text(spatial_observation):
                                self.add_memory_entry(spatial_observation, "spatial observation", sim_step_manager)
        self.situation = self.name+ " is in the " + world.area_grid[self.x][self.y] + " area." +" ".join(descriptions) + " " + self.name + " is holding: " + self.holding if descriptions else "Nothing of interest nearby." 
        print(self.situation)
        self.write_to_records(self.name + "'s situation is the following: "+self.situation)
        if saw_interactable: 
            self.interact(num, sim_step_manager, task_system)