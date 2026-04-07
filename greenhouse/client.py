import requests
from typing import Tuple
from .models import GreenhouseAction, GreenhouseObservation

class GreenhouseClient:
    """
    Emergency Manual Client: 
    Bypasses the broken openenv library to get the simulation running.
    """
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url

    def step(self, action: GreenhouseAction) -> Tuple[GreenhouseObservation, float, bool]:
        payload = action.model_dump() if hasattr(action, 'model_dump') else action.dict()
        response = requests.post(f"{self.server_url}/step", json=payload)
        data = response.json()
        
        obs = GreenhouseObservation(**data['observation'])
        return obs, float(data['reward']), bool(data['done'])

    def reset(self) -> GreenhouseObservation:
        response = requests.post(f"{self.server_url}/reset")
        data = response.json()
        return GreenhouseObservation(**data['observation'])