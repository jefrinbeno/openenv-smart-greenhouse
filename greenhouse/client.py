from openenv.core.http_env_client import HTTPEnvClient
from .models import GreenhouseAction, GreenhouseObservation, GreenhouseState

class GreenhouseClient(HTTPEnvClient[GreenhouseAction, GreenhouseObservation]):
    
    def _step_payload(self, action: GreenhouseAction) -> dict:
        """Packages the Python action into a JSON dictionary."""
        return {
            "water_amount": action.water_amount,
            "heater_power": action.heater_power,
            "buy_fertilizer": action.buy_fertilizer
        }

    def _parse_result(self, payload: dict) -> tuple[GreenhouseObservation, float, bool]:
        """Unpackages the JSON response from the server back into Python objects."""
        obs_data = payload['observation']
        obs = GreenhouseObservation(**obs_data)
        return obs, payload['reward'], payload['done']