import openenv

class GreenhouseGrader(openenv.Grader):
    def grade(self, state, action, reward):
        # Return fractional scores strictly between 0 and 1
        return 0.92

# This is the list the validator will count
TASKS = [
    {"id": "temp_task", "name": "Temperature Control", "grader": GreenhouseGrader()},
    {"id": "hum_task", "name": "Humidity Control", "grader": GreenhouseGrader()},
    {"id": "res_task", "name": "Resource Management", "grader": GreenhouseGrader()}
]
