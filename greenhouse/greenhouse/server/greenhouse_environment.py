from openenv.core.env_server import Environment
from models import GreenhouseAction, GreenhouseObservation, GreenhouseState
from core.weather import WeatherSimulator
from core.physics import PhysicsEngine
from core.rewards import RewardCalculator

class GreenhouseEnvironment(Environment):
    def __init__(self):
        self._state = GreenhouseState(total_reward_accumulated=0.0, is_dead=False)
        self.weather_sim = WeatherSimulator()
        self.physics = PhysicsEngine()
        self.reward_calc = RewardCalculator()
        self.current_day = 1
        self.current_soil_moisture = 50.0
        self.current_temp = 22.0
        self.current_budget = 500
        self.current_crop_health = 100.0
        self.current_weather = self.weather_sim.get_weather()
        super().__init__()

    @property
    def state(self) -> GreenhouseState:
        return self._state

    def reset(self) -> GreenhouseObservation:
        self._state = GreenhouseState(total_reward_accumulated=0.0, is_dead=False)
        self.current_day = 1
        self.current_soil_moisture = 50.0
        self.current_temp = 22.0
        self.current_budget = 500
        self.current_crop_health = 100.0
        self.current_weather = self.weather_sim.get_weather()
        return self._get_obs()

    def step(self, action: GreenhouseAction) -> GreenhouseObservation:
        if self._state.is_dead or self.current_day > 30:
            return self._get_obs()

        self.current_soil_moisture, self.current_temp = self.physics.update(
            self.current_soil_moisture, self.current_temp, action, self.current_weather
        )

        cost = (action.water_amount * 2 + action.heater_power * 5)
        if action.buy_fertilizer: cost += 50
        self.current_budget -= cost

        reward, health_delta = self.reward_calc.calculate(
            self.current_soil_moisture, self.current_temp, action, self.current_budget
        )
        
        self.current_crop_health = max(0, min(100, self.current_crop_health + health_delta))
        self._state.total_reward_accumulated += reward
        self.current_day += 1
        self.current_weather = self.weather_sim.get_weather()

        if self.current_crop_health <= 0 or self.current_budget <= 0:
            self._state.is_dead = True

        return self._get_obs()

    def _get_obs(self) -> GreenhouseObservation:
        return GreenhouseObservation(
            day=self.current_day,
            soil_moisture=round(self.current_soil_moisture, 2),
            temperature=round(self.current_temp, 2),
            budget=self.current_budget,
            weather_forecast=self.current_weather,
            crop_health=round(self.current_crop_health, 2)
        )
