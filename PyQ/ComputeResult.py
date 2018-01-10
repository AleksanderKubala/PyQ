class ComputeResult(object):
    
    def __init__(self, amplitude, bits, probability):
        self.amplitude = amplitude
        self.bits = bits
        self.probability = probability

    def __repr__(self):
        return '(' + str(self.amplitude) + '; ' + str(self.bits) + '; ' + str(self.probability) + ')'

    def __str__(self):
        return str(self.amplitude) + ', ' + str(self.bits) + ', ' + str(self.probability)
        


