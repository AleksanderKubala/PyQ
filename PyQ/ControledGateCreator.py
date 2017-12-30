from PyQ.GateCreator import *

class ControledGateCreator(GateCreator):
    """description of class"""

    def _set_custom_params(self, basegate, params):
        self.offset = min(params) if min(params) <= 0 else 0
        last_qubit = max(params) if max(params) >= 0 else 0
        self.size = basegate.size + abs(self.offset) + last_qubit
        self.dimension = 2**(self.size)
        self.limit = self.dimension

    def _compute_mask(self, params):
        eliminator = 1
        matcher = int('1'*(self.basegate_size), 2)
        matcher = matcher << max(params) if max(params) > 0 else matcher
        for i in range(len(params)):
            if params[i] > 0: params[i] = params[i] + (self.basegate_size - 1)
        for i in range(self.offset + 1, self.offset + self.size):
            eliminator = eliminator << 1
            if (i in params) or (i == 0): eliminator = eliminator | 1
            if i == 0: eliminator << (self.basegate_size - 1)
            #if i > 0: matcher = matcher << 1
        return eliminator, matcher
