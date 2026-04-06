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