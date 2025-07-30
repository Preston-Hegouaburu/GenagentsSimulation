
class SimulationStep:
    sim_step = 1
    new_communications = []
    current_communications = []

    def increment_sim_step(self):
        """Increments the simulation step by 1."""
        self.sim_step += 1
        self.current_communications = self.new_communications
        self.new_communications = []

    def add_communications(self, name, text):
        self.new_communications.append(f"[{name}] {text}")

    def get_communications(self):
        return self.current_communications

    def get_sim_step(self):
        """Returns the current value of the simulation step."""
        return self.sim_step