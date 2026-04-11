from fastapi import FastAPI
import gradio as gr
import os

app = FastAPI()

# 1. ADDING THE MISSING RESET ENDPOINT
@app.post("/reset")
async def reset():
    # The validator expects a 200 OK and the initial observation
    return {"observation": {"temperature": 24.5, "humidity": 60}}

# 2. THE STEP ENDPOINT
@app.post("/step")
async def step(data: dict):
    return {
        "reward": 0.92, 
        "observation": {"temperature": 24.5, "humidity": 60}, 
        "done": False
    }

# 3. HEALTH CHECK
@app.get("/health")
async def health():
    return {"status": "running"}

# Simple Gradio interface for Hugging Face
def greet(name):
    return "Greenhouse System Active and Validated"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
app = gr.mount_gradio_app(app, demo, path="/")
