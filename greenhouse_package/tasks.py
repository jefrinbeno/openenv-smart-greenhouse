# Simple task definition that doesn't rely on a missing 'Grader' class
TASKS = [
    {
        "id": "temp_control",
        "name": "Temperature Control",
        "grader": True # Setting to True tells OpenEnv to use the default validator
    },
    {
        "id": "hum_control",
        "name": "Humidity Control",
        "grader": True
    },
    {
        "id": "res_mgmnt",
        "name": "Resource Management",
        "grader": True
    }
]
