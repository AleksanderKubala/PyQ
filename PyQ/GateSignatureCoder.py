from PyQ.GateSignature import GateSignature
from PyQ.Gatename import Gatename

class GateSignatureCoder(object):
    """description of class"""

    @classmethod
    def encode(cls, request):
        pre = cls._convert_controls(request.controls[0])
        size = str(request.size) if request.size > 1 else ""
        post = cls._convert_controls(request.controls[1])
        return GateSignature(request.gate, pre, post, size)

    @classmethod
    def _convert_controls(cls, controls):
        signature = ""
        if controls:
            controls = list(controls)
            min_range = min(controls) if min(controls) < 0 else 1
            max_range = max(controls) + 1 if max(controls) > 0 else 0
            for i in range(min_range, max_range):
                if i in controls: signature = signature + Gatename.CONTROL
                else: signature = signature + Gatename.IDENTITY
        return signature



