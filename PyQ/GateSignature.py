class GateSignature(object):
    
    def __init__(self, gatename, pre = "", post = "", size = ""):
        self.gatename = gatename
        self.pre = pre
        self.post = post
        self.size = size

    def __str__(self):
        return self.pre + self.gatename + self.size + self.post
        


