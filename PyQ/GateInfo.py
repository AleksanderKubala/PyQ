class GateInfo(object):
   
    def __init__(self, size, matrices, signature, multi, offset = 0, basic = False, is_measurement = False):
        self.offset = offset
        self.size = size
        self.matrices = matrices if isinstance(matrices, list) else list((matrices,))
        self.transformation = self.matrices[0]
        self.signature = signature
        self.multi = multi
        self.basic = basic
        self.is_measurement = is_measurement

    def set_transformation(self, arg):
        if self.is_measurement is True and arg is not None:
            self.transformation = self.matrices[arg]
        else:
            self.transformation = self.matrices[0]
