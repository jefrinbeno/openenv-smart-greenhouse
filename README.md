---
title: Smart Greenhouse Pro
emoji: 🌿
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
---

# Smart Greenhouse Enterprise: Digital Twin Simulation

An industrial-grade environmental simulation designed for Reinforcement Learning (RL) research. This project integrates a FastAPI backend with a Gradio 6.0 frontend, containerized via Docker.

## 🏗️ System Architecture
The project follows a modular, decoupled architecture:
* **Physics Engine:** Simulates thermodynamic and hydration variables.
* **Economic Logic:** Calculates reward signals based on plant health.
* **API Layer (FastAPI):** Exposes /step and /reset endpoints for AI agents.
* **Dashboard (Gradio):** High-fidelity UI for manual telemetry.

## 🚀 Key Features
* **Live Analytics:** Real-time thermal and moisture trend charting.
* **Reward Progression:** Dedicated chart for cumulative RL performance.
* **JSON Metadata:** Machine-readable state objects for debugging.

---
**Project Version:** v4.1 (Stable)
**Developer:** Jefrin Beno J M
