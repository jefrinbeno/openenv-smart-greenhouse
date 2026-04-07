---
title: Smart Greenhouse Enterprise
emoji: 🌿
colorFrom: slate
colorTo: emerald
sdk: docker
pinned: false
app_port: 7860
---

# Smart Greenhouse Enterprise: Reinforcement Learning Interface

An industrial-grade digital twin simulation and monitoring dashboard designed for Reinforcement Learning (RL) research. This project integrates a FastAPI backend with a Gradio 6.0 frontend, containerized via Docker and deployed through a synchronized GitHub Actions pipeline.

## 🏗️ System Architecture

The project follows a modular, decoupled architecture to ensure scalability and ease of integration with external RL agents.

### 📦 Component Breakdown
* **Physics Engine (`greenhouse/core/physics.py`):** Simulates real-world thermodynamic and hydration variables.
* **Economic Logic (`greenhouse/core/rewards.py`):** Calculates reward signals based on plant health and resource consumption.
* **Environment Wrapper (`greenhouse/server/greenhouse_environment.py`):** An OpenAI Gym-style interface for state transitions.
* **API Layer (FastAPI):** Exposes `/step` and `/reset` endpoints for remote AI control.
* **Enterprise Dashboard (Gradio):** A high-fidelity UI for manual intervention and visual analytics.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.12 |
| **Backend Framework** | FastAPI |
| **Frontend UI** | Gradio 6.0 |
| **Data Processing** | Pandas, NumPy |
| **Containerization** | Docker |
| **Deployment CI/CD** | GitHub Actions |
| **Cloud Hosting** | Hugging Face Spaces |

---

## 🚀 Key Features

### 1. Professional Control Interface
The dashboard utilizes a **Slate & Emerald** enterprise theme, offering high-precision sliders for Irrigation Flow Rate and Thermal Output Power.

### 2. Real-Time Telemetry & Visual Analytics
* **Atmospheric Monitoring:** Real-time components for Temperature and Substrate Moisture.
* **Thermal Trends:** Line plots visualizing the variance of internal climate.
* **Economic Progression:** A dedicated chart for Cumulative Reward tracking.

### 3. Machine-Readable State (JSON)
The interface provides a live **JSON Telemetry Output** box for inspecting raw state objects, including nested observations and action history.

### 4. Industrial Audit Logs
A comprehensive, scrollable data table tracks every interaction, providing a historical audit trail of environmental changes and accrued rewards.

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
└── README.md                # Project Documentation
```

---

## 🐳 Docker Deployment

The system is optimized for containerized environments. The Dockerfile uses a multi-stage build philosophy:

```dockerfile
FROM python:3.12
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/code
CMD ["python", "-m", "greenhouse.server.app"]
```

---

**Project:** Smart Greenhouse Digital Twin v4.1
```

### 🚀 Execution Commands to Reflect Changes

Run these in your terminal to force the update to GitHub, which will then push the correct configuration to Hugging Face:

```bash
cd /workspaces/openenv-smart-greenhouse

# 1. Stage the corrected README
git add README.md

# 2. Commit with the specific fix message
git commit -m "Fix: Final Hugging Face YAML configuration in README header"

# 3. Push to GitHub
git push origin main
```

