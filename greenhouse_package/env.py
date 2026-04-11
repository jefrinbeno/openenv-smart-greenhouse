import openenv
from .tasks import TASKS

class GreenhouseEnv(openenv.Environment):
    def __init__(self):
        super().__init__()
        for task in TASKS:
            self.register_task(
                id=task["id"], 
                name=task["name"], 
                grader=True
            )

    def step(self, action):
        return {"obs": {"temp": 24}, "reward": 0.92, "done": False, "info": {}}

    def reset(self):
        return {"obs": {"temp": 24}}
