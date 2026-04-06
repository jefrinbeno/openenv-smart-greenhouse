class RewardCalculator:
    def calculate(self, moisture, temp, co2, nutrients, vpd, action):
        # 1. Liebig's Law Growth Factor (0.0 to 1.0)
        # How 'happy' is the plant with each resource?
        f_moisture = 1.0 if 45 <= moisture <= 70 else 0.2
        f_temp = 1.0 if 20 <= temp <= 28 else 0.3
        f_co2 = min(1.5, co2 / 600) # CO2 over 600ppm boosts growth
        f_nutrients = min(1.0, nutrients / 20)
        
        # The growth is limited by the WORST factor
        growth_efficiency = min(f_moisture, f_temp, f_nutrients) * f_co2
        
        # 2. Economic Sustainability
        # Heavy Water or Heat usage is penalized as 'Waste'
        operational_cost = (action.water_amount * 2) + (action.heater_power * 3)
        
        # 3. Final Score
        reward = (growth_efficiency * 50) - operational_cost
        
        return reward, growth_efficiency
