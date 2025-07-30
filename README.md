This is a generative agent simulation leverageing deep seek, an open scource llm modle, to simulate human like agents as they work together to complete a task.

Running The project:
Step 1: Create a python virtual environment
Step 2: install requironments.txt (simply use pip install -r requirements.txt)
Step 3: Go into the general_functions.py file. Under the first funciton "ask(prompt: str)" on line nine the following is displayed:  "Authorization": "Bearer Your API Key Here". Simply replace the "Your API Key Here" text with your own Open Router API Key, while leaving "Bearer."
An important note: As the LLM model used in this simulation is free, if an Open Router API key is made, it will be able to make 50 free calls to this Deep Seek model, althoug 50 calls is not enough to run very many simulation steps, so a paymment of 10 dollars may need to be made to get the sufficent credits for 1000 API calls to this model.
Step 4: Leave Agents as is, or alter their background. More agents can be added by simply duplicating an existing agent and changing their background information
Step 5: Make sure that all memory.json files are empty, and well as the record.txt file. The contents of these files are not erased acutomatically and will need be be done manually. This is especially important for the memory.json files as if their contents are not only: [], then the initial memory setup will not be done correctly
Step 6: run the "run_sim.py." You should be able to see the records of the agents actions and communicaitons comple in the record.txt file as well as in the terminal