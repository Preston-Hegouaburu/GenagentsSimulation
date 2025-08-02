

# Generative Agent Simulation using DeepSeek

This project simulates human-like generative agents collaborating to complete a task. It leverages **[DeepSeek](https://deepseek.com/)** — a powerful open-source LLM — accessed via the **OpenRouter API**. Each agent is designed to emulate cognitive behaviors such as memory, communication, and reasoning.

---

## Getting Started

Follow these steps to set up and run the simulation:

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## 3. Set Your API Key

Open the file `general_functions.py`.

On **line 9**, locate this line:

```python
"Authorization": "Bearer Your API Key Here"
```

Replace `"Your API Key Here"` with your own [OpenRouter](https://openrouter.ai) API key — **leave `"Bearer "` in place**.

> ⚠️ **Note:**
> The DeepSeek model is free via OpenRouter for up to **50 calls**.
> For extended simulations (\~1000 API calls), you may need to **add \$10 in credit** to your account.

---

## 4. Configure the Agents

* You can use the default agents or modify their backgrounds.
* To add new agents:

  1. Duplicate an existing agent file.
  2. Modify the background information as desired.

---

##  5. Clear Prior State

Before running the simulation:

* Make sure that **all `memory.json` files** contain only:

```json
[]
```

* Clear the contents of `record.txt`.

> If memory files are not reset, agents will retain old data and initialization will not work as intended.

---

## 6. Run the Simulation

Run the simulation script:

```bash
python run_sim.py
```

You will see:

* Agent actions and communication printed in the **terminal**.
* All output also logged in `record.txt`.

---
## Notes

* This is an early prototype exploring agent collaboration.
* You can expand the simulation with new agent goals, tasks, or environments.
* The agents currently rely on a single shared LLM (DeepSeek) for reasoning.

---