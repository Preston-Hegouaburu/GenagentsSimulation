import os
import generalFunctions

sim_step = 0

importance_path = os.path.join("templates", "memory evaluation", "importance.txt")
reasoning_path = os.path.join("templates", "memory evaluation", "reasoning.txt")

def main():
    agents = generalFunctions.load_all_agents()
    while True:
        for agent in agents:
            #agent percives
            #agent adds the observation memory
            #agent reasons over these memories given past ones
            #agent gives each observation and resoning an importance score
            #then comes the response part where the situation is presented along with the most relevant memories to the situatio
            #output is then carried out(no movement at the moment)
            agent.add_memory_entry("Saw a bird fly by.", "observation", sim_step)# Add a memory entry for the first agent
        sim_step += 1


main()
