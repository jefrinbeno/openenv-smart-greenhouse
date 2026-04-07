---
title: Smart Greenhouse Pro
emoji: 🌿
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
---

# Smart Greenhouse Enterprise: Digital Twin Simulation

An industrial-grade environmental simulation designed for Reinforcement Learning (RL) research. This project integrates a FastAPI backend with a Gradio 6.0 frontend, containerized via Docker and deployed through a synchronized GitHub Actions pipeline.

## 🏗️ System Architecture

The project follows a modular, decoupled architecture to ensure scalability and ease of integration with external RL agents.

### 📦 Component Breakdown
* **Physics Engine (`greenhouse/core/physics.py`):** Simulates real-world thermodynamic and hydration variables using differential equations.
* **Economic Logic (`greenhouse/core/rewards.py`):** Calculates reward signals based on plant health, resource consumption, and nutrient efficiency.
* **Environment Wrapper (`greenhouse/server/greenhouse_environment.py`):** An OpenAI Gym-style interface that manages state transitions and resets.
* **API Layer (FastAPI):** Exposes `/step` and `/reset` endpoints for remote headless control.
* **Enterprise Dashboard (Gradio):** A high-fidelity UI for manual intervention and visual analytics.

---

## 🚀 Key Features

### 1. Professional Control Interface
The dashboard utilizes a **Slate & Emerald** enterprise theme, offering high-precision sliders for Irrigation Flow Rate and Thermal Output Power.

### 2. Real-Time Telemetry & Visual Analytics
* **Atmospheric Monitoring:** Real-time components for Temperature and Substrate Moisture.
* **Thermal Trends:** Line plots visualizing the variance of internal climate over time.
* **Economic Progression:** A dedicated chart for Cumulative Reward, essential for evaluating RL model performance.

### 3. Machine-Readable State (JSON)
The interface provides a live **JSON Telemetry Output** box. This allows researchers to inspect the raw state object for RL agent training.

---

## 📂 Project Structure

```text
.
├── .github/workflows/       # CI/CD Sync Scripts
├── greenhouse/
│   ├── core/                # Physics, Rewards, and Weather logic
│   ├── server/
│   │   ├── app.py           # Main Entry Point (FastAPI + Gradio)
│   │   └── environment.py   # RL Environment Wrapper
│   └── models.py            # Pydantic Data Models
├── Dockerfile               # Container Configuration
├── requirements.txt         # Dependency Manifest
├── inferency.py
└── README.md                # Project Documentation
🐳 Docker Deployment
The system is optimized for containerized environments. The Dockerfile uses a multi-stage build philosophy to ensure the environment is identical across all deployment stages.

Project Version: v4.1 (Stable)


---

## 🎮 How to Use the Digital Twin

### 1. Manual Intervention (Gradio)
The **Dashboard** allows you to override the system:
* **Irrigation Flow:** Adjust the `water_amount` to prevent substrate dehydration.
* **Thermal Output:** Control the `heater_power` to maintain the optimal 24°C - 28°C range.
* **Execute Step:** Click to advance the simulation by one time-step and see the physics engine calculate the new state.

### 2. Autonomous Agent Control (API)
External Reinforcement Learning agents can interact with the simulation via HTTP POST requests:
* **Endpoint:** `/step`
* **Payload Structure:**
    ```json
    {
      "water_amount": 0.5,
      "heater_power": 0.3
    }
    ```
* **Response:** Returns a `State` observation, a `Reward` float, and a `Terminal` boolean.

---

## 📈 Reinforcement Learning Logic

### The Reward Function
The system evaluates performance based on a weighted sum of three factors:
1. **Plant Health:** Penalty for extreme temperatures or dry soil.
2. **Resource Efficiency:** Penalty for high water and electricity usage.
3. **Nutrient Stability:** Bonus for maintaining consistent substrate moisture levels.



---

## 🐳 Deployment & CI/CD

This repository is "Live-Synced." On every `git push` to the `main` branch:
1. **GitHub Actions** triggers a synchronization workflow.
2. The code is pushed to **Hugging Face Spaces**.
3. A **Docker** build is initiated, installing all dependencies from `requirements.txt`.
4. The **FastAPI/Gradio** server is deployed as a containerized microservice.



---


