import uvicorn
import pandas as pd
import json
import time
from fastapi import FastAPI
import gradio as gr
from greenhouse.server.greenhouse_environment import GreenhouseEnvironment
from greenhouse.models import GreenhouseAction

# ---------------------------------------------------------
# 1. Backend Engine & Analytics Initialization
# ---------------------------------------------------------
app = FastAPI(title="Smart Greenhouse Pro Enterprise")
env = GreenhouseEnvironment()

# Global state management for industrial-grade logging
# Initializing with a small offset ensures charts have a baseline
state_log = {
    "Step": [],
    "Temperature": [],
    "Moisture": [],
    "Step_Reward": [],
    "Cumulative_Reward": [],
    "Efficiency_Index": [],
    "Timestamp": []
}
step_counter = 0
total_accrued_reward = 0.0

@app.post("/step")
async def api_step(action: GreenhouseAction):
    obs, reward, done = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

@app.post("/reset")
async def api_reset():
    obs = env.reset()
    return {"observation": obs}

# ---------------------------------------------------------
# 2. Advanced Business Logic & UI Processing
# ---------------------------------------------------------
def process_simulation_step(water, heat, fertilizer):
    global step_counter, total_accrued_reward
    
    # 2.1 Action Packaging
    action = GreenhouseAction(
        water_amount=water, 
        heater_power=heat, 
        buy_fertilizer=fertilizer
    )
    
    # 2.2 Execute Physics Step
    obs, reward, done = env.step(action)
    
    # 2.3 Analytics Calculations
    step_counter += 1
    total_accrued_reward += reward
    # Efficiency index calculation for professional visualization
    efficiency = max(0, min(100, (reward + 1) / 2 * 100))
    
    # 2.4 Update Industrial Logs
    state_log["Step"].append(step_counter)
    state_log["Temperature"].append(round(obs.temp, 2))
    state_log["Moisture"].append(round(obs.moisture, 2))
    state_log["Step_Reward"].append(round(reward, 4))
    state_log["Cumulative_Reward"].append(round(total_accrued_reward, 4))
    state_log["Efficiency_Index"].append(round(efficiency, 2))
    state_log["Timestamp"].append(time.strftime("%H:%M:%S"))
    
    df = pd.DataFrame(state_log)
    
    # 2.5 Dynamic Status Reports
    if reward > 0.8:
        status = "Optimal Performance"
    elif reward > 0.4:
        status = "Nominal Operation"
    else:
        status = "Critical Variance Detected"
        
    # 2.6 Generate Machine-Readable State Object (JSON)
    telemetry_json = {
        "metadata": {
            "version": "4.1.0",
            "environment_id": "PU-BANGALORE-SIM-01",
            "last_sync": state_log["Timestamp"][-1]
        },
        "telemetry": {
            "step": step_counter,
            "metrics": {"temp": obs.temp, "moist": obs.moisture},
            "economic_data": {"reward": reward, "total": total_accrued_reward}
        },
        "control_state": action.dict(),
        "is_terminal": done
    }
    
    return (
        f"{obs.temp:.2f} C", 
        f"{obs.moisture:.2f} %", 
        status, 
        f"{total_accrued_reward:.4f}",
        json.dumps(telemetry_json, indent=2),
        df,  # Target for Thermal Chart
        df,  # Target for Reward Chart
        df   # Target for Audit Logs
    )

def industrial_reset():
    global step_counter, total_accrued_reward, state_log
    obs = env.reset()
    step_counter = 0
    total_accrued_reward = 0.0
    for key in state_log: state_log[key] = []
    
    empty_df = pd.DataFrame(columns=state_log.keys())
    return (
        f"{obs.temp:.2f} C", 
        f"{obs.moisture:.2f} %", 
        "System Initialized", 
        "0.0000", 
        "{}", 
        empty_df, 
        empty_df,
        empty_df
    )

# ---------------------------------------------------------
# 3. Enterprise UI Architecture (Slate & Emerald Theme)
# ---------------------------------------------------------
with gr.Blocks(title="Industrial Greenhouse Control") as demo:
    gr.Markdown("""
    # Enterprise Smart Greenhouse Control Interface
    **Digital Twin Simulation & Reinforcement Learning Telemetry Dashboard**
    """)
    
    with gr.Row():
        # -- CONTROL INTERFACE --
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("### Control Parameters")
            water_input = gr.Slider(0, 1, label="Irrigation Flow Rate", value=0.1)
            heat_input = gr.Slider(0, 1, label="Thermal Output Power", value=0.2)
            fert_toggle = gr.Checkbox(label="Automated Nutrient Injection", value=False)
            
            with gr.Row():
                execute_btn = gr.Button("Execute Simulation Step", variant="primary")
                reset_sys_btn = gr.Button("Hard Reset Environment", variant="stop")
            
            gr.Markdown("### Machine-Readable State (JSON)")
            json_explorer = gr.Code(label="JSON Telemetry Output", language="json", interactive=False)

        # -- ANALYTICS DASHBOARD --
        with gr.Column(scale=2):
            gr.Markdown("### Real-Time Telemetry")
            with gr.Row():
                temp_gauge = gr.Label(label="Atmospheric Temperature")
                moist_gauge = gr.Label(label="Soil Moisture Content")
            
            with gr.Row():
                status_box = gr.Textbox(label="Operational Status", interactive=False)
                reward_box = gr.Textbox(label="Accrued Cumulative Reward", interactive=False)

            with gr.Tabs():
                with gr.TabItem("Performance Visualization"):
                    with gr.Row():
                        # High Precision Thermal Chart
                        thermal_plot = gr.LinePlot(
                            label="Thermal Trends",
                            x="Step",
                            y="Temperature",
                            title="Temperature Variance (C)",
                            tooltip=["Step", "Temperature"],
                            y_lim=[15, 40],
                            container=True
                        )
                        # Reward Progression Chart
                        reward_prog_plot = gr.LinePlot(
                            label="Economic Logic Performance",
                            x="Step",
                            y="Cumulative_Reward",
                            title="Cumulative Reward Progression",
                            tooltip=["Step", "Cumulative_Reward"],
                            container=True
                        )
                
                with gr.TabItem("Industrial Audit Logs"):
                    gr.Markdown("### Complete Step-by-Step Historical Audit")
                    audit_table = gr.DataFrame(
                        label="System Logs",
                        interactive=False,
                        wrap=True
                    )

    # ---------------------------------------------------------
    # 4. Event & Data Pipeline Wiring
    # ---------------------------------------------------------
    execute_btn.click(
        fn=process_simulation_step,
        inputs=[water_input, heat_input, fert_toggle],
        outputs=[
            temp_gauge, 
            moist_gauge, 
            status_box, 
            reward_box, 
            json_explorer, 
            thermal_plot, 
            reward_prog_plot,
            audit_table
        ]
    )

    reset_sys_btn.click(
        fn=industrial_reset,
        outputs=[
            temp_gauge, 
            moist_gauge, 
            status_box, 
            reward_box, 
            json_explorer, 
            thermal_plot, 
            reward_prog_plot,
            audit_table
        ]
    )

# ---------------------------------------------------------
# 5. Enterprise Theming & Deployment
# ---------------------------------------------------------
app = gr.mount_gradio_app(
    app, 
    demo, 
    path="/", 
    theme=gr.themes.Soft(
        primary_hue="slate", 
        secondary_hue="emerald",
        neutral_hue="zinc",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
    )
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)