import random

class RandDist:
    '''A random weighted distribution
    construct by providing a dictionary with keys being objects,
    and values corresponding to the weight of the object
    the value of a getting an object = w/total
    where w is the weight of object, and total is the sum of all weights
    '''
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
        '''randomly return an item, based on weight'''
        rand = random.random() * self.total
        last = None
        for weight in self.weights:
            if rand <= weight:
                return self.weighted_items[weight]