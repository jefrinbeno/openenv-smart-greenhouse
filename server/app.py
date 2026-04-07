import uvicorn
import os
import sys

# Ensure the root directory is in the path so greenhouse module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from greenhouse.server.app import app

def main():
    """
    Main entry point for the OpenEnv validator to start the server.
    """
    # The validator expects the server to run on port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
