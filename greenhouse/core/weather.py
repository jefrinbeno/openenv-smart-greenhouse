import random

class WeatherSimulator:
    def __init__(self):
        self.states = ["Sunny", "Cloudy", "Rainy", "Heatwave"]
        # Probability Matrix: [Sunny, Cloudy, Rainy, Heatwave]
        self.transition_matrix = {
            "Sunny": [0.6, 0.2, 0.1, 0.1],
            "Cloudy": [0.3, 0.4, 0.3, 0.0],
            "Rainy": [0.2, 0.5, 0.3, 0.0],
            "Heatwave": [0.4, 0.1, 0.0, 0.5]
        }
        self.current_state = "Sunny"

    def get_weather(self):
        probs = self.transition_matrix[self.current_state]
        self.current_state = random.choices(self.states, weights=probs)[0]
        return self.current_state
