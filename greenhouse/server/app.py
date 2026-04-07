import uvicorn
from fastapi import FastAPI
import gradio as gr
from greenhouse.server.greenhouse_environment import GreenhouseEnvironment
from greenhouse.models import GreenhouseAction

# 1. Initialize the FastAPI Backend
app = FastAPI(title="Smart Greenhouse Pro")
env = GreenhouseEnvironment()

@app.post("/step")
async def step(action: GreenhouseAction):
    obs, reward, done = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

@app.post("/reset")
async def reset():
    obs = env.reset()
    return {"observation": obs}

# 2. Initialize the Gradio Frontend
def ui_step(water, heat, fertilizer):
    action = GreenhouseAction(water_amount=water, heater_power=heat, buy_fertilizer=fertilizer)
    obs, reward, done = env.step(action)
    status = "✅ Healthy" if reward > 0 else "⚠️ Stress"
    return f"{obs.temp}°C", f"{obs.moisture}%", status, f"Score: {reward}"

with gr.Blocks() as demo:
    gr.Markdown("# 🌿 Smart Greenhouse Dashboard")
    with gr.Row():
        t_out = gr.Label(label="Temp")
        m_out = gr.Label(label="Moisture")
    with gr.Row():
        w = gr.Slider(0, 1, label="Water", value=0.1)
        h = gr.Slider(0, 1, label="Heat", value=0.2)
        f = gr.Checkbox(label="Fertilizer")
    btn = gr.Button("Submit Step")
    btn.click(ui_step, inputs=[w, h, f], outputs=[t_out, m_out, gr.Textbox(), gr.Textbox()])

# 3. Mount Gradio onto FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    # Port 7860 is the Hugging Face standard
    uvicorn.run(app, host="0.0.0.0", port=7860)