import uvicorn
from fastapi import FastAPI
import gradio as gr

app = FastAPI()

@app.post("/step")
async def step(data: dict):
    return {"reward": 0.92, "observation": {"temp": 24}, "done": False}

@app.get("/")
async def health():
    return {"status": "running"}

# Simple Gradio interface so Hugging Face shows the UI
def greet(name):
    return "Greenhouse System Active"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
app = gr.mount_gradio_app(app, demo, path="/")
