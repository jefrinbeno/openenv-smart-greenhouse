

```markdown
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
* **Physics Engine (`greenhouse/core/physics.py`):** Simulates real-world thermodynamic and hydration variables using differential equations.
* **Economic Logic (`greenhouse/core/rewards.py`):** Calculates reward signals based on plant health, resource consumption (water/electricity), and nutrient efficiency.
* **Environment Wrapper (`greenhouse/server/greenhouse_environment.py`):** An OpenAI Gym-style interface that manages state transitions and resets.
* **API Layer (FastAPI):** Exposes `/step` and `/reset` endpoints for remote headless control by AI agents.
* **Enterprise Dashboard (Gradio):** A high-fidelity UI for manual intervention, real-time telemetry, and visual analytics.

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
* **Atmospheric Monitoring:** Real-time Label components for Temperature and Substrate Moisture.
* **Thermal Trends:** Line plots visualizing the variance of internal climate over time.
* **Economic Progression:** A dedicated chart for Cumulative Reward, essential for evaluating the learning progress of an RL model.

### 3. Machine-Readable State (JSON)
The interface provides a live **JSON Telemetry Output** box. This allows researchers to inspect the raw state object, including:
* Nested observations (Temp/Moist).
* Dictionary-formatted action history.
* Terminal state flags.

### 4. Industrial Audit Logs
A comprehensive, scrollable data table tracks every interaction with the system, providing a historical audit trail of all environmental changes and accrued rewards.

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

## 💻 Installation & Local Execution

To run the simulation locally, ensure you have Python 3.12+ installed:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/jefrinbeno/openenv-smart-greenhouse.git](https://github.com/jefrinbeno/openenv-smart-greenhouse.git)
    cd openenv-smart-greenhouse
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch the System:**
    ```bash
    export PYTHONPATH=$PYTHONPATH:.
    python greenhouse/server/app.py
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

## 🛡️ Security & CI/CD
This project utilizes **GitHub Actions** for Continuous Deployment. On every push to the `main` branch, the repository is synchronized to Hugging Face Spaces using an encrypted `HF_TOKEN`.

---

**Project:** Smart Greenhouse Digital Twin v4.1
```

---

### 🚀 Execution Commands

Run these to push the fix and clear the configuration error:

```bash
cd /workspaces/openenv-smart-greenhouse
git add README.md
git commit -m "Fix: Added required Hugging Face YAML metadata to README"
git push origin main
```

