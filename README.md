---
title: Smart Greenhouse Enterprise
emoji: 🌿
colorFrom: slate
colorTo: emerald
sdk: docker
pinned: false
app_port: 7860
---

# Smart Greenhouse Enterprise: Digital Twin Simulation
An industrial-grade environmental simulation for Reinforcement Learning research. 
Developed with FastAPI, Gradio 6.0, and Docker.

## 🏗️ System Architecture
The project follows a modular, decoupled architecture to ensure scalability:
* **Backend:** FastAPI managing the `/step` and `/reset` endpoints.
* **Frontend:** Gradio 6.0 "Slate & Emerald" Dashboard.
* **Environment:** Physics-based greenhouse simulation logic.

## 🚀 Key Features
* **Manual Control:** High-precision sliders for Irrigation and Thermal output.
* **Telemetry:** Real-time charts for Temperature and Cumulative Reward.
* **API Access:** Machine-readable JSON state objects for RL agents.

---
**Project Version:** v4.1 (Stable)
