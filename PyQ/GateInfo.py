class GateInfo(object):
   
    def __init__(self, size, matrix, signature, offset = 0):
        self.offset = offset
        self.size = size
        self.matrix = matrix
        self.signature = signature

