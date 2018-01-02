from PyQ.GateCreator import *

class SwapGateCreator(GateCreator):
    """description of class"""

    def _set_custom_params(self, basegate, params):
        self.size = params
        self.limit = 2**(params - 1)
        self.dimension = self.limit*2
        self.multi = True

    def _compute_mask(self, params):
        eliminator = 1
        matcher = (1 << (params - 1)) | 1
        return eliminator, matcher
        
        
    




