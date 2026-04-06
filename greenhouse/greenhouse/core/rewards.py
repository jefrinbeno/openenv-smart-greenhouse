class RewardCalculator:
    def calculate(self, moisture, temp, action, budget):
        reward = 0
        health_delta = 0
        
        # Ideal conditions: 40-70% moisture, 20-28°C temp
        if 40 <= moisture <= 70:
            reward += 10
            health_delta += 2
        else:
            reward -= 5
            health_delta -= 3
            
        if 20 <= temp <= 28:
            reward += 10
            health_delta += 2
        else:
            reward -= 5
            health_delta -= 3
            
        return reward, health_delta
