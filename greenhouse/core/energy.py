class EnergyManager:
    def __init__(self):
        self.battery_capacity = 100.0
        self.current_charge = 50.0

    def update(self, action, weather):
        # 1. Solar Generation
        gen_map = {"Sunny": 15.0, "Heatwave": 20.0, "Cloudy": 5.0, "Rainy": 1.0}
        generation = gen_map.get(weather, 0)
        
        # 2. Consumption
        consumption = (action.heater_power * 4.0) + (action.water_amount * 1.5)
        
        # 3. Battery Math
        self.current_charge = max(0, min(self.battery_capacity, self.current_charge + generation - consumption))
        
        # 4. Grid Cost (If battery is empty, you pay the "Grid Tax")
        grid_usage = max(0, consumption - (self.current_charge + generation))
        return round(self.current_charge, 2), round(grid_usage * 12.0, 2) # $12 per unit grid cost
