import math

class PhysicsEngine:
    def __init__(self):
        self.thermal_inertia = 0.82
        self.co2_decay_rate = 0.1 # CO2 leaks out over time

    def update(self, moisture, temp, co2, nutrients, action, weather_data):
        # 1. Thermal & Vapor Dynamics
        ambient_map = {"Sunny": 30, "Heatwave": 40, "Rainy": 16, "Cloudy": 23}
        t_target = ambient_map.get(weather_data, 25)
        temp = (temp * self.thermal_inertia) + (t_target * (1 - self.thermal_inertia)) + (action.heater_power * 2.8)
        
        # 2. Gas Exchange (CO2)
        # Fertilizer action now includes a CO2 boost option
        co2_gain = 200 if action.buy_fertilizer else 0
        co2 = (co2 * (1 - self.co2_decay_rate)) + co2_gain + 400 # Base atmospheric CO2 is ~400ppm
        
        # 3. Nutrient Uptake (Mass Balance)
        # Faster growth (high temp/light) consumes more nutrients
        uptake_rate = 0.05 * (temp / 20) * (co2 / 400)
        nutrients = max(0, nutrients - uptake_rate + (15 if action.buy_fertilizer else 0))
        
        # 4. Psychrometrics for VPD
        es = 0.611 * math.exp((17.27 * temp) / (temp + 237.3))
        ea = es * (moisture / 100.0)
        vpd = es - ea
        
        # 5. Transpiration
        transpiration = 0.06 * vpd * (temp / 30)
        moisture = max(0, min(100, moisture + (action.water_amount * 4.0) - transpiration))
        
        return moisture, round(temp, 2), round(co2, 1), round(nutrients, 2), round(vpd, 3)
