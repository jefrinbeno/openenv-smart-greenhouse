from pydantic import BaseModel

class GreenhouseState(BaseModel):
    temperature: float = 22.0
    moisture: float = 50.0
    energy_level: float = 100.0

class GreenhouseAction(BaseModel):
    water_amount: float
    heater_power: float
    buy_fertilizer: bool = False

class GreenhouseObservation(BaseModel):
    temp: float
    moisture: float