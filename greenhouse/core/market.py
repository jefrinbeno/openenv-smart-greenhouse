import random

class MarketSimulator:
    def __init__(self):
        self.price_multiplier = 1.0

    def update(self):
        # Stochastic Price Fluctuations
        self.price_multiplier = max(0.5, min(2.5, self.price_multiplier + random.uniform(-0.3, 0.3)))
        return round(self.price_multiplier, 2)

    def get_demand_status(self):
        if self.price_multiplier > 1.8: return "CRITICAL DEMAND (High Payout)"
        if self.price_multiplier < 0.8: return "OVERSUPPLY (Low Value)"
        return "STABLE"
