It looks like the formatting broke again when you copied it\! When you copy from a webpage instead of raw text, all the code blocks (` ```python `), tables, and bold formatting disappear.

Here is the **final, completely fixed, 100% formatted raw markdown**.

### 🛑 CRITICAL INSTRUCTIONS:

**Do not highlight the text to copy it.** Instead, click the small **"Copy code"** button in the top right corner of the black box below. Then paste it into your `README.md` file in VS Code and hit save.

````markdown
# 🌿 Greenhouse Precision Agriculture Simulator
**A High-Fidelity Digital Twin for Resource-Constrained Reinforcement Learning**

[![OpenEnv Framework](https://img.shields.io/badge/Framework-OpenEnv-blue.svg)](https://github.com/openenv/openenv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deployment](https://img.shields.io/badge/Deployed_on-Hugging_Face-orange.svg)](https://huggingface.co/spaces/jefrinbeno35/smart-greenhouse)

---

## 📖 Executive Summary & Vision

The **Greenhouse Precision Agriculture Simulator** transcends standard Reinforcement Learning (RL) "toy environments" by implementing a rigorous, non-linear mathematical model of a smart agricultural system. 

Designed for the SST Hackathon 2026, this environment challenges artificial agents to manage a 30-day crop lifecycle. The agent must balance complex biological imperatives (e.g., maintaining Vapor Pressure Deficit thresholds) with external economic pressures, including stochastic weather patterns and volatile energy grid pricing. 

Success in this environment requires an agent to move beyond reactive policies and learn **anticipatory resource allocation**, optimizing a multi-variate "Sustainability Index" rather than simply maximizing an unbounded score.

---

## 🏛️ System Architecture

The project is structured as a decoupled client-server architecture, built on the **OpenEnv** framework, allowing for low-latency RL training via WebSockets. 

### 📂 Directory Structure
```text
openenv-smart-greenhouse/
├── greenhouse/
│   ├── config/
│   │   ├── __init__.py
│   │   └── default.yaml
│   ├── core/                  # 🧠 The Simulation Engine
│   │   ├── __init__.py
│   │   ├── energy.py          # Micro-Grid & Battery Logic
│   │   ├── market.py          # Crop Price Volatility
│   │   ├── physics.py         # Thermodynamics & VPD
│   │   ├── rewards.py         # Liebig's Law & RL Signal
│   │   └── weather.py         # Markov-Chain Weather
│   ├── server/                # 🌐 The Interface Layer
│   │   ├── __init__.py
│   │   ├── app.py             # FastAPI & WebSockets
│   │   ├── Dockerfile         # Container Blueprint
│   │   ├── greenhouse_environment.py # OpenEnv Integration
│   │   └── requirements.txt
│   ├── tests/
│   ├── __init__.py
│   ├── client.py              # RL Client SDK
│   ├── models.py              # Action/Observation Pydantic Schemas
│   ├── openenv.yaml           # Framework Manifest
│   ├── pyproject.toml
│   └── README.md              # Project Documentation
├── .gitignore
└── pytest.ini
````

### 1\. The Core Simulation Engine (`greenhouse/core/`)

The `core/` directory acts as the central "Brain" of the digital twin, housing specialized intelligence nodes that simulate real-world physics and economics.

  * **`physics.py` (Thermodynamics & Psychrometrics)**
      * *Function:* Handles state transitions for environmental variables based on Newtonian laws rather than linear step-functions.
      * *Mechanics:* Calculates thermal inertia, heat dissipation rates, and relative humidity impacts.
  * **`rewards.py` (Economic Shaping & Biological Bottlenecks)**
      * *Function:* Computes the continuous reward signal ($R_t$) used by the RL agent.
      * *Mechanics:* Translates physical plant health and financial efficiency into a unified optimization scalar.
  * **`energy.py` (Micro-Grid Simulation)**
      * *Function:* Simulates a localized energy grid featuring solar generation and battery storage limits.
      * *Mechanics:* Forces the agent to learn "Demand Response"—heating the greenhouse when solar energy is abundant to avoid "Grid Tax" penalties during night cycles.
  * **`weather.py` (Environmental Stochasticity)**
      * *Function:* Acts as the primary external perturbation source.
      * *Mechanics:* Utilizes a Markov-Chain Transition Matrix to generate realistic, non-independent weather forecasting (e.g., a "Heatwave" is more likely to follow a "Sunny" day than a "Rainy" day).
  * **`market.py` (FinTech Integration)**
      * *Function:* Introduces a secondary objective: financial profitability.
      * *Mechanics:* Implements stochastic price volatility for the final crop harvest, requiring the agent to time biological growth stages with market demand spikes.

### 2\. The Interface Layer (`greenhouse/server/`)

  * **`greenhouse_environment.py`:** The central hub that instantiates the OpenEnv `Environment` base class. It synchronizes the sub-modules (Physics, Market, Energy) and exposes the `reset()` and `step()` functions to the API.
  * **`app.py`:** A high-performance FastAPI server that wraps the environment logic, exposing both RESTful HTTP endpoints for state inspection and WebSocket endpoints for low-latency agent training.
  * **`Dockerfile`:** Defines the containerized runtime environment, ensuring parity between local development and Hugging Face cloud deployment.

### 3\. The Data Models (`greenhouse/models.py`)

Utilizes Pydantic schemas to strictly define the input (Action) and output (Observation) spaces, ensuring type safety across the network boundary.

-----

## 🎮 The Reinforcement Learning Interface

### 🕹️ Action Space (`GreenhouseAction`)

The agent manages three critical control vectors at every time step ($t$):

1.  **`water_amount` (Continuous/Discrete int):** Irrigation volume. Overwatering leads to root rot penalties; underwatering halts transpiration.
2.  **`heater_power` (Continuous/Discrete int):** Thermal energy input. High usage rapidly drains the battery grid.
3.  **`buy_fertilizer` (Boolean):** A strategic financial decision to inject Nitrogen and $CO_2$. Costs a flat fee from the budget.

### 👁️ Observation Space (`GreenhouseObservation`)

The agent perceives a high-dimensional state vector ($S_t \in \mathbb{R}^n$):

  * **`day` (int):** Current step in the 30-day episode horizon.
  * **`soil_moisture` (float %):** Current volumetric water content.
  * **`temperature` (float °C):** Internal climate reading.
  * **`budget` (float $):** Remaining operational capital. Reaching $\le 0$ terminates the episode (`done = True`).
  * **`weather_forecast` (string):** Contextual data providing the current weather state, the plant's biological stage (Sprout $\rightarrow$ Harvest), and Market Status.
  * **`crop_health` (float %):** Integrity of the biological system. Reaching $\le 0$ terminates the episode (`done = True`).

### 📈 The Multi-Objective Reward Function

The agent is optimized via a composite reward signal designed to favor sustainable precision agriculture:

$$R_t = (G_e \times 50) - (C_{op} + C_{tax})$$

  * $G_e$: Growth Efficiency (from Liebig's Law).
  * $C_{op}$: Operational Base Costs (Water pumping + standard electricity).
  * $C_{tax}$: Carbon Tax / Grid Penalty. An exponential financial penalty applied if the agent uses high `heater_power` while the `battery_charge` is depleted, forcing reliance on "Peak Grid" energy.

-----

## 🚀 Professional Quick Start Guide

Designed for seamless integration with industry-standard RL libraries such as Stable Baselines3 or Ray RLLib.

### 1\. Installation

Clone the repository and install the OpenEnv framework:

```bash
git clone https://github.com/jefrinbeno/openenv-smart-greenhouse
cd openenv-smart-greenhouse
pip install openenv
```

### 2\. Client-Side Agent Loop

Connect to the production-grade Hugging Face container to train an agent without running the server locally:

```python
from greenhouse import GreenhouseAction, GreenhouseEnv

# Connect via WebSockets to the live Hugging Face deployment
with GreenhouseEnv.from_env("jefrinbeno35/smart-greenhouse") as env:
    
    # Initialize the 30-day episode
    obs = env.reset()
    print(f"Episode Started. Initial Budget: ${obs.observation.budget}")
    
    # Example: A Heuristic/Strategic Agent Loop
    for day in range(1, 31):
        
        action = GreenhouseAction(
            water_amount=5 if obs.observation.soil_moisture < 45 else 0,
            heater_power=3 if obs.observation.temperature < 20 else 0,
            buy_fertilizer=True if day % 7 == 0 else False
        )
        
        obs = env.step(action)
        
        if obs.done:
            print("Episode Terminated (Harvested, Bankrupt, or Withered).")
            break
```

-----

## 🌐 Live Deployment & Interactive Documentation

The environment is containerized via Docker and continuously deployed to Hugging Face Spaces.

| Interface Type | Description | Access Link |
| :--- | :--- | :--- |
| **Interactive Dashboard** | A Gradio-based web UI allowing human users to play the "Game" and test the physics engine manually. | [Launch Web UI](https://huggingface.co/spaces/jefrinbeno35/smart-greenhouse/web) |
| **API Documentation** | Full OpenAPI / Swagger documentation detailing the REST endpoints, Schemas, and WebSocket protocols. | [View API Docs](https://www.google.com/search?q=https://huggingface.co/spaces/jefrinbeno35/smart-greenhouse/docs) |
| **Health Monitoring** | A lightweight endpoint to verify container uptime and FastApi responsiveness. | [Check Status](https://www.google.com/search?q=https://huggingface.co/spaces/jefrinbeno35/smart-greenhouse/health) |

-----

## 🏆 Technical Differentiation & Hackathon Relevance

Most Hackathon RL submissions rely on simple grid-worlds or linear state progressions (e.g., "If water \> 5, health + 1").

This project was built to simulate **Systemic Collapse Dynamics**. If an agent makes a mistake in Day 3 (e.g., over-heating the greenhouse), the **Newtonian thermal inertia** ensures that the temperature will stay dangerously high for Days 4 and 5, even if the agent turns the heater off.

This creates a **Lagged Control Problem**. The agent cannot simply react to the current observation; it must **anticipate** the future state of the thermodynamics and the energy grid. By forcing the agent to respect thermal inertia, battery storage constraints, and nutrient bottlenecks, this environment filters for sophisticated, forward-thinking policy networks.

-----

## 🔬 Appendix A: Deep-Dive Implementation Details

To fully understand the complexity of the digital twin, below are the exact mechanics and mathematical models driving the `core/` intelligence nodes.

### 1\. The Thermodynamics Engine (`physics.py`)

Standard environments use simple linear addition for temperature (e.g., `temp += heater_power`). Our environment uses a discretized version of **Newton's Law of Cooling** combined with Joule heating.

**The Equation:**
$$T_{t+1} = T_{ext} + (T_t - T_{ext}) \cdot e^{-k \Delta t} + (\eta \cdot P_{heater})$$

  * $T_t$: Internal temperature at current step.
  * $T_{ext}$: External ambient temperature (driven by the Markov weather state).
  * $k$: Thermal leakage coefficient of the greenhouse materials (glass/polycarbonate).
  * $P_{heater}$: Action input from the RL agent.
  * $\eta$: Heating efficiency multiplier.

**Psychrometrics & VPD:**
Plant transpiration is governed by the Vapor Pressure Deficit (VPD). We calculate Saturation Vapor Pressure ($e_s$) using the Tetens equation:
$$e_s = 0.6108 \cdot \exp\left(\frac{17.27 \cdot T}{T + 237.3}\right)$$
This forces the agent to realize that heating the greenhouse drastically increases the VPD, risking plant dehydration if not offset by increased irrigation.

### 2\. The Micro-Grid Battery Logic (`energy.py`)

The greenhouse does not have infinite free energy. It is connected to a localized solar-plus-storage grid.

  * **Solar Generation Profile:**
      * `Sunny`: +15.0 kWh/step
      * `Cloudy`: +5.0 kWh/step
      * `Rainy`: +1.0 kWh/step
  * **Consumption:** The heater draws exactly $4.0 \text{ kWh}$ per unit of power, and the water pump draws $1.5 \text{ kWh}$.
  * **The Grid Tax Penalty:** If the agent drains the $100 \text{ kWh}$ battery capacity to $0$, the system automatically pulls from the municipal grid. The grid charges a punitive "Peak Rate" of **$12 per unit**, which rapidly bankrupts agents that fail to pre-heat the greenhouse during solar peak hours.

### 3\. Biological Bottlenecks (`rewards.py`)

The reward function utilizes **Liebig's Law of the Minimum**. An agent cannot compensate for zero water by providing maximum fertilizer.

**The Algorithm:**

```python
def calculate_growth(moisture, temp, nutrients, co2):
    # Normalize all resources to a 0.0 - 1.0 biological happiness scale
    f_moisture = 1.0 if 45 <= moisture <= 70 else 0.2
    f_temp = 1.0 if 20 <= temp <= 28 else 0.3
    f_nutrients = min(1.0, nutrients / 20.0)
    
    # Growth is strictly bottlenecked by the LOWEST factor
    base_growth = min(f_moisture, f_temp, f_nutrients)
    
    # CO2 acts as an atmospheric multiplier
    co2_multiplier = min(1.5, co2 / 600.0)
    
    return base_growth * co2_multiplier
```

This non-linear scalar is then multiplied by 50 to generate the positive reinforcement signal, directly opposing the negative financial signals generated by the `energy.py` module.

### 4\. Stochastic Weather Transitions (`weather.py`)

Weather is not chosen at random (`random.choice()`); it follows a highly realistic **Markov-Chain Transition Matrix**.

| Current State | $\rightarrow$ Sunny | $\rightarrow$ Cloudy | $\rightarrow$ Rainy | $\rightarrow$ Heatwave |
| :--- | :--- | :--- | :--- | :--- |
| **Sunny** | 60% | 20% | 5% | 15% |
| **Cloudy** | 30% | 40% | 30% | 0% |
| **Rainy** | 10% | 50% | 40% | 0% |
| **Heatwave**| 40% | 10% | 0% | 50% |

This requires the RL agent to learn **Transition Probabilities**. For instance, if the current weather is `Heatwave`, the agent must learn that there is a 0% chance of rain tomorrow, meaning it must irrigate heavily today to prepare.

### 5\. OpenEnv Integration & Schema (`models.py`)

To ensure type safety across the WebSocket boundary, we enforce strict Pydantic models.

```python
class GreenhouseAction(BaseModel):
    water_amount: int = Field(ge=0, le=20, description="Liters of water to pump")
    heater_power: int = Field(ge=0, le=10, description="HVAC heating intensity")
    buy_fertilizer: bool = Field(default=False, description="Spend $150 for NPK/CO2 injection")

class GreenhouseObservation(BaseModel):
    day: int
    soil_moisture: float
    temperature: float
    budget: float
    weather_forecast: str
    crop_health: float
```

By enforcing these bounds (`ge=0`, `le=20`), we prevent the RL agent from exploring physically impossible state spaces (like pumping negative water), massively speeding up the training convergence time.

-----