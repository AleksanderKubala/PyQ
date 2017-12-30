import numpy
from PyQ.GateCreatorResult import GateCreatorResult

class GateCreator(object):
    """description of class"""

    def __init__(self, **kwargs):
        self.basegate_size = 0;
        self.basegate_dim = 0
        self.size = 0
        self.dimension = 0
        self.limit = 0
        self.offset = 0

    def create(self, basegate, params):
        self._set_creator_params(basegate, params)
        eliminator, matcher = self._compute_mask(params)
        group_list = self._create_groups(eliminator, matcher)
        matrix = self._create_gate(basegate, group_list)
        return GateCreatorResult(matrix, self.size, self.offset)

    def _set_creator_params(self, basegate, params):
        self.basegate_size = basegate.size
        self.basegate_dim = 2**basegate.size
        self._set_custom_params(basegate, params)

    def _create_groups(self, eliminator, matcher):
        group_list, group = list(), list()
        for i in range(eliminator, self.limit):
            if (i & eliminator) == eliminator:
                group.append(i)
                group.append(i^matcher)
                if len(group) >= self.basegate_dim:
                    group_list.append(sorted(group))
                    group = list()
        return group_list

    def _create_gate(self, basegate, group_list):
        output = numpy.identity(self.dimension, dtype = complex)
        for group in group_list:
            for i in range(self.basegate_dim):
                for j in range(self.basegate_dim):
                    output[group[i]][group[j]] = basegate.matrix.item((i, j))
        return output

    def _set_custom_params(self, basegate, params):
        raise NotImplementedError("setting at least 'self.dimension' and 'self.limit' attributes required")

    def _compute_mask(self, params):
        raise NotImplementedError