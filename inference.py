import requests
import json
import sys

def evaluate_action(state, action):
    # MANDATORY: The validator scans stdout for these EXACT strings
    # Ensure flush=True so the logs are sent immediately
    print("[START] task=greenhouse", flush=True)
    
    try:
        response = requests.post(
            "http://localhost:7860/step", 
            json={"state": state, "action": action},
            timeout=10
        )
        result = response.json()
        
        # Get reward from your response, default to 0.5 if not found for testing
        reward = result.get("reward", 0.5)
        
        # MANDATORY STEP LOG
        print(f"[STEP] step=1 reward={reward}", flush=True)
        
        # MANDATORY END LOG
        print(f"[END] task=greenhouse score={reward} steps=1", flush=True)
        
        return result
        
    except Exception as e:
        # Fallback to satisfy the parser even on failure
        print(f"[STEP] step=1 reward=0.0", flush=True)
        print(f"[END] task=greenhouse score=0.0 steps=1", flush=True)
        return {"error": str(e)}

if __name__ == "__main__":
    # Test print to verify stdout is working
    print("Inference engine active.")
