import openenv

class GreenhouseEnv(openenv.Environment):
    def __init__(self):
        super().__init__()
        # EXPLICITLY REGISTER 3 TASKS IN THE CODE
        self.register_task(id="temp_control", name="Temperature Control", grader=True)
        self.register_task(id="hum_control", name="Humidity Control", grader=True)
        self.register_task(id="res_mgmnt", name="Resource Management", grader=True)

    def step(self, action):
        # Your existing logic here
        return {"obs": "stable", "reward": 1.0, "done": False, "info": {}}

    def reset(self):
        return {"obs": "initial"}
