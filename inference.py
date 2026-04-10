import requests
import json
import sys

def evaluate_action(state, action):
    """
    Interface for the OpenEnv validator with mandatory structured logging.
    """
    # 1. Print the START block
    print(f"[START] task=greenhouse_management", flush=True)
    
    try:
        # 2. Call your server
        response = requests.post(
            "http://localhost:7860/step", 
            json={"state": state, "action": action},
            timeout=10
        )
        result = response.json()
        
        # Extract reward and observation (adjust keys if your JSON is different)
        reward = result.get("reward", 0.0)
        
        # 3. Print the STEP block (MANDATORY for Output Parsing)
        print(f"[STEP] step=1 reward={reward}", flush=True)
        
        # 4. Print the END block with a final score
        print(f"[END] task=greenhouse_management score={reward} steps=1", flush=True)
        
        return result
        
    except Exception as e:
        print(f"Error during inference: {e}", file=sys.stderr)
        # Even on error, try to print an END block to satisfy the parser
        print(f"[END] task=greenhouse_management score=0 steps=0", flush=True)
        return {"error": str(e)}

if __name__ == "__main__":
    # Small test if run directly
    print("Inference engine ready for structured output.")
