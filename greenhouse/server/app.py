import uvicorn
import pandas as pd
from fastapi import FastAPI
import gradio as gr
from greenhouse.server.greenhouse_environment import GreenhouseEnvironment
from greenhouse.models import GreenhouseAction

# 1. Initialize the FastAPI Backend
app = FastAPI(title="Smart Greenhouse Pro")
env = GreenhouseEnvironment()

# Persistent state for live charts and history
history = {"Step": [], "Temperature": [], "Moisture": [], "Reward": []}
step_count = 0

@app.post("/step")
async def step(action: GreenhouseAction):
    obs, reward, done = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

@app.post("/reset")
async def reset():
    obs = env.reset()
    return {"observation": obs}

# 2. UI Logic
def ui_step(water, heat, fertilizer):
    global step_count
    action = GreenhouseAction(
        water_amount=water, 
        heater_power=heat, 
        buy_fertilizer=fertilizer
    )
    
    obs, reward, done = env.step(action)
    step_count += 1
    
    history["Step"].append(step_count)
    history["Temperature"].append(round(obs.temp, 2))
    history["Moisture"].append(round(obs.moisture, 2))
    history["Reward"].append(round(reward, 4))
    
    df = pd.DataFrame(history)
    status = "System Healthy" if reward > 0 else "Stress Detected"
    
    return (
        f"{obs.temp:.2f} C", 
        f"{obs.moisture:.2f} %", 
        status, 
        f"Score: {reward:.4f}",
        df, 
        df.tail(10)
    )

def ui_reset():
    global step_count, history
    obs = env.reset()
    step_count = 0
    history = {"Step": [], "Temperature": [], "Moisture": [], "Reward": []}
    empty_df = pd.DataFrame(columns=["Step", "Temperature", "Moisture", "Reward"])
    return (
        f"{obs.temp:.2f} C", 
        f"{obs.moisture:.2f} %", 
        "System Reset", 
        "Score: 0.0000", 
        empty_df, 
        empty_df
    )

# 3. Professional Interface Layout
with gr.Blocks() as demo:
    gr.Markdown("# Smart Greenhouse Pro Dashboard")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Control Panel")
            water_ctrl = gr.Slider(0, 1, label="Water Pump", value=0.1)
            heat_ctrl = gr.Slider(0, 1, label="Heater Power", value=0.2)
            fert_ctrl = gr.Checkbox(label="Apply Fertilizer", value=False)
            
            with gr.Row():
                btn = gr.Button("Submit Step", variant="primary")
                reset_btn = gr.Button("Reset Simulation", variant="stop")
            
        with gr.Column(scale=2):
            gr.Markdown("### Live Telemetry")
            with gr.Row():
                temp_out = gr.Label(label="Temperature")
                moist_out = gr.Label(label="Moisture")
            
            with gr.Row():
                status_msg = gr.Textbox(label="System Status", interactive=False)
                reward_msg = gr.Textbox(label="Reward Signal", interactive=False)

    with gr.Tabs():
        with gr.TabItem("Visual Trends"):
            with gr.Row():
                # Removed 'overlay_point' to fix TypeError
                temp_chart = gr.LinePlot(
                    label="Climate History",
                    x="Step",
                    y="Temperature",
                    title="Temperature (C)",
                    tooltip=["Step", "Temperature"]
                )
                moist_chart = gr.LinePlot(
                    label="Hydration History",
                    x="Step",
                    y="Moisture",
                    title="Moisture (%)",
                    tooltip=["Step", "Moisture"]
                )
        
        with gr.TabItem("Step Logs"):
            gr.Markdown("### Historical Data (Recent 10 Steps)")
            history_table = gr.DataFrame(
                headers=["Step", "Temperature", "Moisture", "Reward"],
                datatype=["number", "number", "number", "number"]
            )

    btn.click(
        ui_step, 
        inputs=[water_ctrl, heat_ctrl, fert_ctrl], 
        outputs=[temp_out, moist_out, status_msg, reward_msg, temp_chart, history_table]
    ).then(
        lambda df: df, inputs=[temp_chart], outputs=[moist_chart]
    )

    reset_btn.click(
        ui_reset, 
        outputs=[temp_out, moist_out, status_msg, reward_msg, temp_chart, history_table]
    ).then(
        lambda df: df, inputs=[temp_chart], outputs=[moist_chart]
    )

app = gr.mount_gradio_app(
    app, 
    demo, 
    path="/", 
    theme=gr.themes.Soft(primary_hue="slate", secondary_hue="gray")
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)