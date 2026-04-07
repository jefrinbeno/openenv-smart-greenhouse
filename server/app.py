import sys
import os

# Add the current directory to path so it can find the greenhouse module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from greenhouse.server.app import app, main

if __name__ == "__main__":
    main()
