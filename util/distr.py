import random

class RandDist:
    def __init__(self, weighted_items):
        self.total = 0.0
        for value in weighted_items.values():
            self.total += value
        # remapping 
        self.weights = []
        self.weighted_items = {}
        current = 0.0
        for item in weighted_items:
            current += weighted_items[item]
            self.weighted_items[current] = item
            self.weights.append(current)
        
    def get(self):
        rand = random.random() * self.total
        last = None
        for weight in self.weights:
            if rand <= weight:
                return self.weighted_items[weight]