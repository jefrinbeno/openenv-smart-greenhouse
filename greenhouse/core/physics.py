class GreenhousePhysics:
    def update(self, temp, moisture, heater, water):
        # Thermal inertia + external cooling
        new_temp = temp + (heater * 0.15) - 0.08
        # Evaporation + irrigation
        new_moisture = moisture + (water * 0.25) - 0.12
        return round(new_temp, 2), round(new_moisture, 2)
