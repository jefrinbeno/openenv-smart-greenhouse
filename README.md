---
title: OpenEnv Smart Greenhouse
emoji: 🌿
colorFrom: green
colorTo: green
sdk: docker
pinned: false
---

# 🌿 OpenEnv: Smart Greenhouse Digital Twin (Phantom Tenant Architecture)

![Phase 2 Validation](https://img.shields.io/badge/OpenEnv_Scaler-Phase_2_PASSED-success)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🎥 [Click Here to Watch the 60-Second Demo Video](INSERT_YOUR_YOUTUBE_LINK_HERE)

---

## 📂 Comprehensive Repository Architecture

The codebase is strictly modularized to separate core physics mathematical engines from the API routing and UI components. This ensures maximum testability and compliance with the OpenEnv Phase 2 autograder.

```text
openenv-smart-greenhouse/
├── .github/workflows/
│   └── sync_to_hf.yml          # Automated CI/CD to Hugging Face
├── greenhouse/                 # Research-Grade Digital Twin Logic
│   ├── config/
│   │   └── default.yaml        # Universal Environmental Constants
│   └── core/
│       ├── energy.py           # HVAC Thermodynamics & COP Logic
│       ├── market.py           # Dynamic Energy Pricing Models
│       ├── physics.py          # Heat Transfer & Hydrology Engine
│       ├── rewards.py          # Gaussian Multi-Objective Rewards
│       └── weather.py          # Stochastic Diurnal Disturbance Gen
├── greenhouse_package/         # API & Autograder Integration
│   ├── env.py                  # Main RL Environment Orchestrator
│   ├── env_server.py           # Dual-Headed (FastAPI + Gradio)
│   └── tasks.py                # Autograder Schema Path-Mapping
├── server/                     # Production Deployment Layer
│   ├── app.py                  # Uvicorn Entry Point (ASGI)
│   └── Dockerfile              # Multi-Stage Containerization
├── tests/                      # Enterprise Quality Assurance
│   ├── test_endpoints.py       # REST API Handshake Validation
│   ├── test_physics.py         # Thermodynamic Boundary Tests
│   └── test_rewards.py         # Reward-Hacking Prevention Tests
├── openenv.yaml                # Phase 2 Task Manifest (Pydantic Mapped)
├── inference.py                # Scaler Validation Agent
└── requirements.txt            # Dependency Matrix
```

---

## 🧠 Mathematical Formulations & Physics Engine

Our environment utilizes continuous Markovian state evaluations grounded in actual thermodynamic and agricultural science.

### 1. Thermodynamic Heat Transfer (`physics.py`)
We simulate internal temperature fluctuations ($T$) using a modified Newton’s Law of Cooling, integrated with solar radiation ($S$) and HVAC thermal work.
$$T_{t+1} = T_t + \alpha_{hvac}(T_{target} - T_t) + \beta_{insulation}(T_{ext} - T_t) + \gamma \cdot S_t$$

### 2. Vapor Pressure Deficit (VPD) Logic
VPD is the critical agricultural metric measuring the drying power of the air. We derive it using the **Magnus-Tetens** formula for Saturation Vapor Pressure ($e_s$):
$$e_s = 0.6108 \cdot \exp\left(\frac{17.27 \cdot T_{actual}}{T_{actual} + 237.3}\right)$$

The final VPD is then calculated relative to internal humidity ($H$):
$$VPD = e_s \cdot \left(1 - \frac{H_{actual}}{100}\right)$$

### 3. HVAC Coefficient of Performance (COP) & Energy
Energy usage scales dynamically based on the thermal delta. The COP degrades non-linearly as the environment reaches extreme differentials:
$$COP = \max(1.5, 4.0 - 0.05 \cdot |T_{ext} - T_{target}|)$$

Total energy consumption ($E_t$) in kWh is derived from the work required to shift air mass density ($\rho$) across a specific heat capacity ($C_p$):
$$E_t = \frac{|T_{t+1} - T_t| \cdot V \cdot \rho \cdot C_p}{COP \cdot 3600}$$

---

## ⚙️ Markov Decision Process (MDP) Definition

### The Observation Space ($S$)
A continuous vector tracking 7 critical environmental dimensions provided to the agent at each timestep:
$$S = [T_{int}, H_{int}, M_{soil}, T_{ext}, S_{rad}, VPD, B_{mass}]$$

### The "Goldilocks" Reward Function ($R$)
The agent is optimized via a multi-objective Gaussian decay function. This ensures the agent is rewarded for staying in optimal agricultural zones while being penalized for energy expenditure ($E_t$) and grid costs ($P_t$).
$$R_t = \sum_{i \in \{T, H, M\}} \exp\left(-\frac{(x_i - \mu_i)^2}{2\sigma_i^2}\right) - (w_E \cdot E_t \cdot P_t) - \text{Penalty}_{anomaly}$$

---

## 🛡️ Phase 2 Validation & Dual-Headed Routing

To satisfy the strict automated validation schema without sacrificing the complex Human UI, this project utilizes a **Dual-Headed Routing Strategy** inside `env_server.py`:

1. **The Autograder API:** Hidden `@app.post("/reset")` and `@app.post("/step")` routes handle strict JSON handshakes for the Scaler bot, returning 200 OK responses with exact Pydantic-validated payloads.
2. **The Schema Bypass:** The `openenv.yaml` utilizes string-path mapping to `tasks.py`, bypassing typical Pydantic drops during Phase 2 evaluation.
3. **The UI Overlay:** A customized Gradio interface is mounted directly onto the FastAPI instance via `gr.mount_gradio_app()`. This provides a visual command center for humans while the bot communicates with the backend via REST.

---

## 🚀 Deployment & Installation

### Local Docker Build
```bash
docker build -t greenhouse-env .
docker run -p 7860:7860 greenhouse-env
```

### Direct Python Execution
```bash
pip install -r requirements.txt
python -m uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### Interface Endpoints
* **Human Dashboard:** `http://localhost:7860`
* **RL API Endpoint:** `POST http://localhost:7860/step`

---
*Architected and Developed by Jefrin Beno J M, Nandana Sajikumar, and Hema Priya for the OpenEnv x Scaler Hackathon 2026.*
```

