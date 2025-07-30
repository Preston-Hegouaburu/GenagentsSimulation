import heapq
import csv
import os
class Tile:
    def __init__(self):
        self.events = [None, None, None, None]  # 4 event slots

    def add_event(self, event):
        for i in range(len(self.events)):
            if self.events[i] is None:
                self.events[i] = event
                return True
        return False  # No empty slot available

    def remove_event(self, event):
        for i in range(len(self.events)):
            if self.events[i] == event:
                self.events[i] = None
                return True
        return False

    def __repr__(self):
        return f"Tile(events={self.events})"


class World:
    def __init__(self):
        
        self.width = 19
        self.height = 19
        
        # Memory grid (tiles with events)
        self.area_grid = [["None" for _ in range(self.width)] for _ in range(self.height)]

        self.memory_grid = [[Tile() for _ in range(self.width)] for _ in range(self.height)]
        # Collision grid (True = collidable, False = walkable)
        self.collision_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

    def load_areas_from_csv(self):
        mapping = {
            "0": {"Area": "Storage Area"},
            "1": {"Area": "Meatal Gathering Area"},
            "2": {"Area": "Wood Collecting Area"},
            "3": {"Area": "Water Gathering Area"},
            "4": {"Area": "Food Gathering Area"},
        }
        csv_file = os.path.join("world", "world-1-areas.csv")
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            for y, row in enumerate(reader):
                for x, value in enumerate(row):
                    if value not in mapping:
                        continue  # Ignore unknown values
                    area = mapping[value]
                    self.area_grid[x][y] = area["Area"]

    def load_world_from_csv(self):
        self.load_areas_from_csv()
        mapping = {
            "0": {"walkable": True},
            "X": {"walkable": False},
            "M": {"walkable": True, "event": "Task 0"},
            "W": {"walkable": True, "event": "Task 1"},
            "WA": {"walkable": True, "event": "Task 3"},
            "F": {"walkable": True, "event": "Task 4"},
            "C": {"walkable": True, "event": "Task 5"},
            "EM": {"walkable": True, "event": "Area Spawn: Metal"},
            "EW": {"walkable": True, "event": "Area Spawn: Wood"},
            "EWA": {"walkable": True, "event": "Area Spawn: Water"},
            "EF": {"walkable": True, "event": "Area Spawn: Food"},
            "EC": {"walkable": True, "event": "Area Spawn: Storage"}
        }
        csv_file = os.path.join("world", "world-1.csv")
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            for x, row in enumerate(reader):
                for y, value in enumerate(row):
                    if value not in mapping:
                        print("no workie")
                        continue  # Ignore unknown values
                    tile_info = mapping[value]

                    # Set collision
                    if "walkable" in tile_info:
                        self.collision_grid[x][y] = not tile_info["walkable"]
                    
                    # Add events
                    if "event" in tile_info:
                        self.memory_grid[x][y].add_event(tile_info["event"])

    def set_collidable(self, x, y, collidable=True):
        """Mark a tile as collidable or walkable."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.collision_grid[y][x] = collidable

    def add_event_to_tile(self, x, y, event):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.memory_grid[y][x].add_event(event)
        return False

    def remove_event_from_tile(self, x, y, event):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.memory_grid[y][x].remove_event(event)
        return False
    
    def is_walkable(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and not self.collision_grid[y][x]
        

    def display(self, agent_list=None):
        """ASCII visualization of the grid."""
        print("\nWorld:")
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if self.collision_grid[y][x]:
                    row.append("#")  # Collidable block
                elif agent_list and any(a.x == x and a.y == y for a in agent_list):
                    row.append("A")  # Agent
                elif any(self.memory_grid[y][x].events):
                    row.append("E")  # Event
                else:
                    row.append(".")
            record_path = os.path.join(base_dir, 'record.txt')
            with open(record_path, "a") as file:
                file.write(" ".join(row) + "\n")
            print(" ".join(row))
        print()