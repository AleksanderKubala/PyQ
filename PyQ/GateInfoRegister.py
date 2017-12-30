from PyQ.GateInfo import GateInfo
from PyQ.GateRequest import GateRequest
from PyQ.GateSignatureCoder import GateSignatureCoder as GSC
from PyQ.GateSignature import GateSignature
from PyQ.ControledGateCreator import ControledGateCreator as CGC
from PyQ.SwapGateCreator import SwapGateCreator as SGC
from PyQ.Gate import Gate
from PyQ.Gatename import Gatename
import numpy


class GateInfoRegister(object):
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            return GateInfoRegister()
        else:
            return cls._instance

    _instance = None
    _ic = 'ic'

    def __init__(self):
        if(self._instance is None):
            self.register = {}
            self.h_factor = 1/(numpy.sqrt(2))
            self._initialize_register()
            self._instance = self

    def _initialize_register(self):
        self.register[Gatename.IDENTITY] = GateInfo(1, numpy.matrix([[1, 0],[0, 1]]), GateSignature(Gatename.IDENTITY))
        self.register[Gatename.HADAMARD] = GateInfo(1, self.h_factor*numpy.matrix([[1, 1],[1, -1]]), GateSignature(Gatename.HADAMARD))
        self.register[Gatename.PAULI_X] = GateInfo(1, numpy.matrix([[0, 1],[1, 0]]), GateSignature(Gatename.PAULI_X))
        self.register[Gatename.PAULI_Y] = GateInfo(1, numpy.matrix([[0, -1j],[1j, 0]]), GateSignature(Gatename.PAULI_Y))
        self.register[Gatename.PAULI_Z] = GateInfo(1, numpy.matrix([[1, 0],[0, -1]]),  GateSignature(Gatename.PAULI_Z))
        self.register[Gatename.S] = GateInfo(1, numpy.matrix([[1, 0],[0, 1j]]),  GateSignature(Gatename.S))
        self.register[Gatename.T] = GateInfo(1, numpy.matrix([[1, 0],[0, numpy.cos(numpy.pi/4) + 1j*numpy.sin(numpy.pi/4)]]),  GateSignature(Gatename.T))
        self.register[Gatename.SWAP + "2"] = GateInfo(2, SGC().create(self.register[Gatename.NOT], 2).matrix, GateSignature(Gatename.SWAP, size = "2"))
        self.register[Gatename.CONTROL + Gatename.NOT] = GateInfo(2, CGC().create(self.register[Gatename.NOT], [-1]).matrix, GateSignature(Gatename.NOT, pre = Gatename.CONTROL), offset = -1)
        self.register[Gatename.CONTROL + Gatename.CONTROL + Gatename.NOT] = GateInfo(3, CGC().create(self.register[Gatename.NOT], [-2, -1]).matrix, GateSignature(Gatename.NOT, pre = Gatename.CONTROL + Gatename.CONTROL), offset = -2)


    def get(self, request):
        signature = GSC.encode(request)
        gateinfo = self._check_register(signature)
        if gateinfo is None:
            result = self._call_creator(request)
            if result is None:  
                return None
            gateinfo = self.add(request, result, signature)
        pre, post = [], []
        qubits = [request.qubit] if request.size == 1 else [request.qubit, request.qubit + request.size - 1]
        controls = [pre + qubits[0] for pre in request.controls[0]] + [post + qubits[-1] for post in request.controls[1]]
        return Gate(gateinfo, qubits, request.gate, controls)

    def add(self, request, result, signature):
        gateinfo = GateInfo(result.size, result.matrix, signature, result.offset)
        self.register[str(signature)] = gateinfo
        return gateinfo

    def _call_creator(self, request):
        result = None
        control = True if request.controls[0] or request.controls[1] else False
        swap = True if request.gate == Gatename.SWAP else False
        if control and swap:
            result = self._controled_swap(request)
        elif control:
            result = self._call_controled_creator(request.basegate, request.controls[0] + request.controls[1])
        elif swap:
            result = self._call_swap_creator(request.size)
        return result

    def _call_controled_creator(self, basegate, params):
        return CGC().create(self.register[basegate], params)

    def _call_swap_creator(self, params):
        if params < 2: raise ValueError("Size of SWAP gate must by at least 2. Passed: {0}".format(params))
        return SGC().create(self.register[Gatename.NOT], params)
        
    def _controled_swap(self, request):
        swap_request = GateRequest(request.gate, request.qubit, size = request.size)
        self.get(swap_request)
        return self._call_controled_creator(swap_request.basegate, request.controls[0] + request.controls[1])

    def _check_register(self, signature):
        try: 
            gateinfo = self.register[str(signature)]
        except KeyError: 
            return None
        return gateinfo
        






