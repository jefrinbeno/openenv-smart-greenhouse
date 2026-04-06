class PhysicsEngine:
    def update(self, moisture, temp, action, weather):
        # Apply action effects
        moisture += (action.water_amount * 2.5)
        temp += (action.heater_power * 1.5)
        
        # Apply weather effects
        if weather == "Sunny":
            temp += 1.0; moisture -= 2.0
        elif weather == "Heatwave":
            temp += 3.0; moisture -= 5.0
        elif weather == "Rainy":
            temp -= 1.0; moisture += 4.0
            
        # Natural decay
        moisture -= 1.5
        temp -= 0.5
        
        return max(0, min(100, moisture)), max(0, min(50, temp))
