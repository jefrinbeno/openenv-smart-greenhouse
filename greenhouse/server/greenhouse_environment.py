from ..models import GreenhouseAction, GreenhouseObservation, GreenhouseState
from ..core.physics import GreenhousePhysics

# We create a dummy base class since the library is broken
class Environment:
    def __init__(self): pass

class GreenhouseEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.physics = GreenhousePhysics()
        self.state = GreenhouseState()

    def step(self, action: GreenhouseAction):
        self.state.temperature, self.state.moisture = self.physics.update(
            self.state.temperature, self.state.moisture, 
            action.heater_power, action.water_amount
        )
        obs = GreenhouseObservation(temp=self.state.temperature, moisture=self.state.moisture)
        reward = 1.0 if (21 <= self.state.temperature <= 24) else -0.1
        return obs, reward, False

    def reset(self):
        self.state = GreenhouseState()
        return GreenhouseObservation(temp=self.state.temperature, moisture=self.state.moisture)