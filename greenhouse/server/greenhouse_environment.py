from openenv.core.env_server import Environment
from models import GreenhouseAction, GreenhouseObservation, GreenhouseState
from core.weather import WeatherSimulator
from core.physics import PhysicsEngine
from core.rewards import RewardCalculator
from core.energy import EnergyManager
from core.market import MarketSimulator

class GreenhouseEnvironment(Environment):
    def __init__(self):
        self._state = GreenhouseState(total_reward_accumulated=0.0, is_dead=False)
        self.physics = PhysicsEngine()
        self.reward_calc = RewardCalculator()
        self.weather_sim = WeatherSimulator()
        self.energy_mgr = EnergyManager()
        self.market = MarketSimulator()
        self.reset()
        super().__init__()

    @property
    def state(self): return self._state

    def reset(self):
        self._state = GreenhouseState(total_reward_accumulated=0.0, is_dead=False)
        self.day, self.moisture, self.temp = 1, 60.0, 24.0
        self.co2, self.nutrients, self.health = 400.0, 50.0, 100.0
        self.budget, self.progress = 1200, 0.0
        self.weather = self.weather_sim.get_weather()
        return self._get_obs()

    def step(self, action: GreenhouseAction):
        if self._state.is_dead or self.day >= 30: return self._get_obs()

        # 1. Update Energy & Market
        battery, grid_cost = self.energy_mgr.update(action, self.weather)
        price_mult = self.market.update()

        # 2. Update Physics
        self.moisture, self.temp, self.co2, self.nutrients, vpd = self.physics.update(
            self.moisture, self.temp, self.co2, self.nutrients, action, self.weather
        )

        # 3. Budget & Rewards
        base_cost = (150 if action.buy_fertilizer else 0)
        self.budget -= (base_cost + grid_cost)
        
        reward, growth_eff = self.reward_calc.calculate(self.moisture, self.temp, self.co2, self.nutrients, vpd, action)
        
        # Harvest Bonus scaled by Market
        if self.progress >= 100:
            self.budget += (500 * price_mult)
            reward += (500 * price_mult)

        self._state.total_reward_accumulated += reward
        self.progress += (growth_eff * 4.0)
        
        # Health Logic
        health_penalty = 8 if (self.moisture < 20 or self.temp > 40 or self.nutrients < 2) else -3
        self.health = max(0, min(100, self.health - health_penalty))

        self.day += 1
        self.weather = self.weather_sim.get_weather()
        if self.health <= 0 or self.budget <= 0: self._state.is_dead = True
        return self._get_obs()

    def _get_obs(self):
        stages = ["Sprout", "Seedling", "Vegetative", "Budding", "Flowering", "Harvest"]
        idx = min(int(self.progress / 20), len(stages)-1)
        market_info = self.market.get_demand_status()
        
        return GreenhouseObservation(
            day=self.day, soil_moisture=round(self.moisture, 2),
            temperature=round(self.temp, 2), budget=int(self.budget),
            weather_forecast=f"{self.weather} | {stages[idx]} | Market: {market_info}",
            crop_health=round(self.health, 2)
        )
