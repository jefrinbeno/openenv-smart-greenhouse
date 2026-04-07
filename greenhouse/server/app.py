import gradio as gr
from greenhouse.client import GreenhouseClient
from greenhouse.models import GreenhouseAction

# Initialize the client (talks to your local or deployed server)
client = GreenhouseClient()

def update_greenhouse(water, heat, fertilizer):
    # 1. Create the action object
    action = GreenhouseAction(
        water_amount=water, 
        heater_power=heat, 
        buy_fertilizer=fertilizer
    )
    
    # 2. Send to the simulation
    obs, reward, done = client.step(action)
    
    # 3. Return the results for the UI
    status = "✅ Healthy" if reward > 0 else "⚠️ Stress Detected"
    return f"{obs.temp}°C", f"{obs.moisture}%", status, f"Score: {reward}"

# Build the Interface
with gr.Blocks(title="Smart Greenhouse Control") as demo:
    gr.Markdown("# 🌿 Smart Greenhouse Dashboard")
    
    with gr.Row():
        temp_out = gr.Label(label="Current Temp")
        moist_out = gr.Label(label="Current Moisture")
    
    with gr.Row():
        water_ctrl = gr.Slider(0, 1, label="Water Pump", value=0.1)
        heat_ctrl = gr.Slider(0, 1, label="Heater Power", value=0.2)
        fert_ctrl = gr.Checkbox(label="Apply Fertilizer")
        
    btn = gr.Button("Submit Step")
    
    msg = gr.Textbox(label="System Status")
    reward_msg = gr.Textbox(label="RL Reward Signal")

    btn.click(update_greenhouse, 
              inputs=[water_ctrl, heat_ctrl, fert_ctrl], 
              outputs=[temp_out, moist_out, msg, reward_msg])

if __name__ == "__main__":
    demo.launch()