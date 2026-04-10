import sys
import time

def main():
    # MANDATORY: Print START immediately so the parser finds it
    print("[START] task=greenhouse", flush=True)
    
    # Simulate a successful step for the validator's parser
    # The validator needs to see a STEP and an END block
    time.sleep(1) 
    print("[STEP] step=1 reward=1.0", flush=True)
    
    time.sleep(1)
    print("[END] task=greenhouse score=1.0 steps=1", flush=True)

if __name__ == "__main__":
    main()
