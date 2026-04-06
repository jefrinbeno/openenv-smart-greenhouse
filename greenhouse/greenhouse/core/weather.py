import random

class WeatherSimulator:
    def __init__(self):
        self.weather_types = ["Sunny", "Cloudy", "Rainy", "Heatwave"]

    def get_weather(self):
        return random.choice(self.weather_types)
