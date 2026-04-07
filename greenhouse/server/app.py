import uvicorn
import pandas as pd
import json
from fastapi import FastAPI
import gradio as gr
from greenhouse.server.greenhouse_environment import GreenhouseEnvironment
from greenhouse.models import GreenhouseAction

# 1. Initialize the FastAPI Backend
app = FastAPI(title="Smart Greenhouse Pro")
env = GreenhouseEnvironment()

# Persistent state for analytics
history = {"Step": [], "Temperature": [], "Moisture": [], "Reward": [], "Cumulative_Reward": []}
step_count = 0
total_reward = 0.0

@app.post("/step")
async def step(action: GreenhouseAction):
    obs, reward, done = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

@app.post("/reset")
async def reset():
    obs = env.reset()
    return {"observation": obs}

# 2. UI Logic with JSON and Analytics
def ui_step(water, heat, fertilizer):
    global step_count, total_reward
    action = GreenhouseAction(
        water_amount=water, 
        heater_power=heat, 
        buy_fertilizer=fertilizer
    )
    
    obs, reward, done = env.step(action)
    step_count += 1
    total_reward += reward
    
    # Update Analytics Data
    history["Step"].append(step_count)
    history["Temperature"].append(round(obs.temp, 2))
    history["Moisture"].append(round(obs.moisture, 2))
    history["Reward"].append(round(reward, 4))
    history["Cumulative_Reward"].append(round(total_reward, 4))
    
    df = pd.DataFrame(history)
    
    # Professional Status Logic
    status = "Operational" if reward > 0 else "Environmental Stress"
    
    # Generate JSON Output for RL Debugging
    json_output = {
        "step": step_count,
        "state": {"temp": obs.temp, "moisture": obs.moisture},
        "action_taken": action.dict(),
        "reward": reward,
        "cumulative_reward": total_reward,
        "terminal": done
    }
    
    return (
        f"{obs.temp:.2f} C", 
        f"{obs.moisture:.2f} %", 
        status, 
        f"{total_reward:.4f}",
        json.dumps(json_output, indent=2),
        df, 
        df.tail(15)
    )

def ui_reset():
    global step_count, total_reward, history
    obs = env.reset()
    step_count = 0
    total_reward = 0.0
    history = {"Step": [], "Temperature": [], "Moisture": [], "Reward": [], "Cumulative_Reward": []}
    empty_df = pd.DataFrame(columns=["Step", "Temperature", "Moisture", "Reward", "Cumulative_Reward"])
    
    return (
        f"{obs.temp:.2f} C", 
        f"{obs.moisture:.2f} %", 
        "System Reset", 
        "0.0000", 
        "{}", 
        empty_df, 
        empty_df
    )

# 3. Professional Interface Design
with gr.Blocks(title="Greenhouse Control Systems") as demo:
    gr.Markdown("""
    # Smart Greenhouse Control Systems
    **Enterprise Environmental Simulation & Reinforcement Learning Interface**
    """)
    
    with gr.Row():
        # Configuration Panel
        with gr.Column(scale=1):
            gr.Markdown("### Control Configuration")
            water_ctrl = gr.Slider(0, 1, label="Hydration Intensity", value=0.1)
            heat_ctrl = gr.Slider(0, 1, label="Thermal Output", value=0.2)
            fert_ctrl = gr.Checkbox(label="Enable Nutrient Supplement", value=False)
            
            with gr.Row():
                btn = gr.Button("Execute Step", variant="primary")
                reset_btn = gr.Button("Reset Environment", variant="stop")
            
            gr.Markdown("### Step Metadata (JSON)")
            json_display = gr.Code(label="State Object", language="json", interactive=False)

        # Analytics Panel
        with gr.Column(scale=2):
            gr.Markdown("### System Telemetry")
            with gr.Row():
                temp_out = gr.Label(label="Internal Temperature")
                moist_out = gr.Label(label="Substrate Moisture")
            
            with gr.Row():
                status_msg = gr.Textbox(label="Operational Status", interactive=False)
                reward_msg = gr.Textbox(label="Cumulative Reward", interactive=False)

            with gr.Tabs():
                with gr.TabItem("Performance Analytics"):
                    with gr.Row():
                        temp_chart = gr.LinePlot(
                            label="Thermal Trends",
                            x="Step",
                            y="Temperature",
                            title="Temperature (C)",
                            tooltip=["Step", "Temperature"],
                            y_lim=[10, 45]
                        )
                        reward_chart = gr.LinePlot(
                            label="Reward Progression",
                            x="Step",
                            y="Cumulative_Reward",
                            title="Cumulative Reward",
                            tooltip=["Step", "Cumulative_Reward"]
                        )
                
                with gr.TabItem("Data Logs"):
                    history_table = gr.DataFrame(label="Simulation History")

    # Event Wiring
    btn.click(
        ui_step, 
        inputs=[water_ctrl, heat_ctrl, fert_ctrl], 
        outputs=[temp_out, moist_out, status_msg, reward_msg, json_display, temp_chart, history_table]
    ).then(
        # Update moisture chart using the same dataframe
        lambda df: df, inputs=[temp_chart], outputs=[temp_chart] 
    )

    reset_btn.click(
        ui_reset, 
        outputs=[temp_out, moist_out, status_msg, reward_msg, json_display, temp_chart, history_table]
    )

# 4. Global Theming and Launch
# Using a slate/zinc professional theme
app = gr.mount_gradio_app(
    app, 
    demo, 
    path="/", 
    theme=gr.themes.Soft(
        primary_hue="slate", 
        secondary_hue="emerald",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui"]
    )
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)