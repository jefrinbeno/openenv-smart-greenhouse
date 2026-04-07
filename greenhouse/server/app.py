import uvicorn
import pandas as pd
from fastapi import FastAPI
import gradio as gr
from greenhouse.server.greenhouse_environment import GreenhouseEnvironment
from greenhouse.models import GreenhouseAction

# 1. Initialize the FastAPI Backend
app = FastAPI(title="Smart Greenhouse Pro")
env = GreenhouseEnvironment()

# Persistent state for live charts
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

# 2. Enhanced UI Logic
def ui_step(water, heat, fertilizer):
    global step_count
    action = GreenhouseAction(
        water_amount=water, 
        heater_power=heat, 
        buy_fertilizer=fertilizer
    )
    
    obs, reward, done = env.step(action)
    step_count += 1
    
    # Update History for Charts
    history["Step"].append(step_count)
    history["Temperature"].append(obs.temp)
    history["Moisture"].append(obs.moisture)
    history["Reward"].append(reward)
    
    df = pd.DataFrame(history)
    
    status = "✅ Healthy" if reward > 0 else "⚠️ Stress Detected"
    reward_color = "green" if reward > 0 else "red"
    
    return (
        f"{obs.temp:.2f}°C", 
        f"{obs.moisture:.2f}%", 
        status, 
        f"Score: {reward:.4f}",
        df # For the charts
    )

# 3. Professional Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="green", secondary_hue="emerald")) as demo:
    gr.Markdown("""
    # 🌿 Smart Greenhouse Pro Dashboard
    ### Real-time Environment Monitoring & RL Control System
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🎛️ Control Panel")
            water_ctrl = gr.Slider(0, 1, label="💧 Water Pump", value=0.1)
            heat_ctrl = gr.Slider(0, 1, label="🔥 Heater Power", value=0.2)
            fert_ctrl = gr.Checkbox(label="💊 Apply Fertilizer", value=False)
            btn = gr.Button("Submit Step", variant="primary")
            
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Live Telemetry")
            with gr.Row():
                temp_out = gr.Label(label="Temperature")
                moist_out = gr.Label(label="Moisture")
            
            with gr.Row():
                status_msg = gr.Textbox(label="System Status", interactive=False)
                reward_msg = gr.Textbox(label="RL Reward Signal", interactive=False)

    with gr.Row():
        gr.Markdown("### 📈 Environmental Trends")
    
    with gr.Row():
        temp_chart = gr.LinePlot(
            label="Climate History",
            x="Step",
            y="Temperature",
            tooltip=["Step", "Temperature"],
            width=500,
            title="Temperature (°C)"
        )
        moist_chart = gr.LinePlot(
            label="Hydration History",
            x="Step",
            y="Moisture",
            tooltip=["Step", "Moisture"],
            width=500,
            title="Moisture (%)"
        )

    # Wire up the logic
    btn.click(
        ui_step, 
        inputs=[water_ctrl, heat_ctrl, fert_ctrl], 
        outputs=[temp_out, moist_out, status_msg, reward_msg, temp_chart]
    ).then(
        lambda df: df, inputs=[temp_chart], outputs=[moist_chart]
    )

# 4. Mount and Launch
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    # Standard Hugging Face Port
    uvicorn.run(app, host="0.0.0.0", port=7860)