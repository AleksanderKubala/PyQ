import random

class RandomValueGenerator(object):

    @classmethod
    def uniform(cls, lower_bound, upper_bound):
        return random.uniform(lower_bound, upper_bound)

    @classmethod
    def discrete_distribution(cls, probabilities, values = None):
        bound = probabilities[0]
        roll = cls.uniform(0, 1)
        value = None
        i = 1
        while bound <= roll:
            bound = bound + probabilities[i]
            i += 1
            if bound > 1:
                raise ValueError("Probabilities are out of range (0, 1)")
        if values is None:
            return i-1
        else:
            return values[i-1]

    @classmethod
    def binary_distribution(cls, truth_probability):
        bound = 1 - truth_probability
        roll = cls.uniform(0, 1)
        if(roll <= bound):
            return False
        else:
            return True