import requests
import json

def evaluate_action(state, action):
    """
    Interface for the OpenEnv validator to interact with the greenhouse.
    """
    try:
        # The validator runs this inside the container where the server is on 7860
        response = requests.post(
            "http://localhost:7860/step", 
            json={"state": state, "action": action},
            timeout=5
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Small local test
    print("Inference script initialized.")
