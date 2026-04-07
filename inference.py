import os
from openai import OpenAI
from greenhouse.server.environment import GreenhouseEnvironment  # Adjust path if needed

# 1. Environment Variables (Required by Checklist)
# Set your active model name as the default for the evaluator
API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "your-chosen-model-here") 
HF_TOKEN = os.getenv("HF_TOKEN") # DO NOT set a default here

# 2. Configure OpenAI Client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_inference():
    # START Log (Required Format)
    print("START")
    
    env = GreenhouseEnvironment()
    obs = env.reset()
    done = False
    step_count = 0

    while not done and step_count < 10:
        # STEP Log (Required Format)
        print(f"STEP {step_count}")
        
        # Example: LLM call using the configured variables
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"State: {obs}. What action?"}]
        )
        
        # Logic to parse LLM response and call env.step() would go here
        # obs, reward, done, info = env.step(action)
        
        step_count += 1

    # END Log (Required Format)
    print("END")

if __name__ == "__main__":
    run_inference()