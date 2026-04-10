def get_ai_optimized_state(raw_data):
    """
    Transforms raw sensor data into descriptive strings to help the 
    LLM Agent understand the environment state better.
    """
    return {
        "current_temperature": f"{raw_data.get('temp', 0)}C",
        "humidity_level": f"{raw_data.get('hum', 0)}%",
        "status_report": "Temperature is above optimal range" if raw_data.get('temp', 0) > 28 else "Conditions stable",
        "recommended_goal": "Maintain moisture while reducing heat"
    }
