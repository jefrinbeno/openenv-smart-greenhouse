from pydantic import BaseModel
from openenv.core.env_server import Action, Observation, State

class GreenhouseAction(Action, BaseModel):
    water_amount: int
    heater_power: int
    buy_fertilizer: bool

class GreenhouseObservation(Observation, BaseModel):
    day: int
    soil_moisture: float
    temperature: float
    budget: int
    weather_forecast: str 
    crop_health: float

class GreenhouseState(State, BaseModel):
    total_reward_accumulated: float
    is_dead: bool
