import random

class RandomValueGenerator(object):

    @classmethod
    def uniform(cls, lower_bound, upper_bound):
        return random.uniform(lower_bound, upper_bound)

    @classmethod
    def discrete_distribution(cls, probabilities, values = None):
        bound = 0
        roll = cls.uniform(0, 1)
        value = None
        for i in range(0, len(probabilities)):
            bound = bound + probabilities[i]
            if roll <= bound:
                value = i
            if bound > 1:
                return ValueError("Probabilities are out of range (0, 1)")
        if values is None:
            return value
        else:
            return values[value]

    @classmethod
    def binary_distribution(cls, truth_probability):
        bound = 1 - truth_probability
        roll = cls.uniform(0, 1)
        if(roll < bound):
            return False
        else:
            return True