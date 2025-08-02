import os
from agent import Agent
import scentence_similarity
from sim_step_manager import SimulationStep
from tile_world import World
from tasks import Tasks

tasks = Tasks()
world = World()
world.load_world_from_csv()
sim_step_manager = SimulationStep()
world.add_event_to_tile(9, 9, "Central Storage")


def load_all_agents(base_dir='agents'):
    agents = []
    i = 0
    for name in os.listdir(base_dir):
        i+=1
        agent_path = os.path.join(base_dir, name)
        print(name)
        if os.path.isdir(agent_path):
            agents.append(Agent(name, 9+i, 9, sim_step_manager, base_dir))
            world.add_event_to_tile(9+i, 9, name)
    return agents


def run_sim_loop():
    agents = load_all_agents()
    world.display(agents)
    
    #agents[0].evaluate_importance()

    #What now: well now that agents can get memories and have personalitys, they have still used nothing, next step is reasoning, so we need memory retrival, so to do that we need memory relevalce and memory importance. After this works communicaitons are next.
    #while True:
    # current plan: I am going to make the physical part to then be able to accurately test the memory retirval by actually being able to give a situation to the agents
    # Next I am going to get movement piece working, and thenthe conversation part working from this point, that should be the majority, then only experimentation and refinement needs to be done, should be done by tommorrow
    for i in range(70):
        for agent in agents:
            agent.observe_surroundings(world, sim_step_manager, tasks)
            agent.evaluate_importance()
            agent.communicate_or_move(world, sim_step_manager)
            agent.reflect(sim_step_manager)
            #if Agent.communicate_or_move() == "move":
            #    agent.bla
            #agent gives each observation and resoning an importance score W
            #then comes the response part where the situation is presented along with the most relevant memories to the situatio W
            #output is then carried out(no movement at the moment) N/A
            #agent.add_memory_entry("Saw a bird fly by.", "observation", sim_step)# Add a memory entry for the first agent
        sim_step_manager.increment_sim_step()
        world.display(agents)
        record_path = os.path.join('agents', 'record.txt')
        with open(record_path, "a") as file:
            file.write(tasks.get_num_items_in_center_storage() + "\n")
            file.write(tasks.get_center_storage_string() + "\n")
            file.write("\n" + "\n" + "The new sim step is: " + str(sim_step_manager.get_sim_step()) + "\n" + "\n")

run_sim_loop()
