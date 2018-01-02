class GateInfo(object):
   
    def __init__(self, size, matrix, signature, multi, offset = 0, basic = False):
        self.offset = offset
        self.size = size
        self.matrix = matrix
        self.signature = signature
        self.multi = multi
        self.basic = basic

