from PyQ.GateInfo import GateInfo
from PyQ.GateRequest import GateRequest
from PyQ.GateSignatureCoder import GateSignatureCoder as GSC
from PyQ.GateSignature import GateSignature
from PyQ.ControledGateCreator import ControledGateCreator as CGC
from PyQ.SwapGateCreator import SwapGateCreator as SGC
from PyQ.Gate import Gate
from PyQ.Gatename import Gatename, Modifier
import numpy
from sympy import *


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
        if self._instance is None:
            self.register = {}
            self.h_factor = sympify(1/sqrt(2))
            self._initialize_register()
            self._instance = self

    def _initialize_register(self):
        self.register[Gatename.MEASUREMENT] = GateInfo(1, [numpy.matrix([[1, 0], [0, 0]]), numpy.matrix([[0, 0], [0, 1]])], Gatename.MEASUREMENT, multi=False, basic=True, is_measurement=True)
        self.register[Gatename.IDENTITY] = GateInfo(1, numpy.matrix([[1, 0],[0, 1]]), GateSignature(Gatename.IDENTITY), multi=False)
        self.register[Gatename.H] = GateInfo(1, self.h_factor * numpy.matrix([[1, 1], [1, -1]]), GateSignature(Gatename.H), multi=False, basic=True)
        self.register[Gatename.X] = GateInfo(1, numpy.matrix([[0, 1], [1, 0]]), GateSignature(Gatename.X), multi=False, basic=True)
        self.register[Gatename.Y] = GateInfo(1, numpy.matrix([[0, -1 * I], [1 * I, 0]]), GateSignature(Gatename.Y), multi=False, basic=True)
        self.register[Gatename.Z] = GateInfo(1, numpy.matrix([[1, 0], [0, -1]]), GateSignature(Gatename.Z), multi=False, basic=True)
        self.register[Gatename.S] = GateInfo(1, numpy.matrix([[1, 0],[0, 1*I]]),  GateSignature(Gatename.S), multi=False, basic=True)
        self.register[Gatename.S_HERMITIAN] = GateInfo(1, numpy.matrix([[1, 0],[0, -1*I]]), GateSignature(Gatename.S + '*'), false, basic=True)
        self.register[Gatename.T] = GateInfo(1, numpy.matrix([[1, 0],[0, exp((pi/4)*I)]]),  GateSignature(Gatename.T), multi=False, basic=True)
        self.register[Gatename.T_HERMITIAN] = GateInfo(1, numpy.matrix([[1, 0],[0, -1*I*exp((pi/4)*I)]]), GateSignature(Gatename.T + '*'), multi=False, basic=True)
        self.register[Gatename.SWAP + "2"] = GateInfo(2, SGC().create(self.register[Gatename.NOT], 2).matrix, GateSignature(Gatename.SWAP, size = "2"), multi=True, basic=True)
        self.register[Modifier.CONTROL + Gatename.NOT] = GateInfo(2, CGC().create(self.register[Gatename.NOT], [-1]).matrix, GateSignature(Gatename.NOT, pre = Modifier.CONTROL), offset = -1, multi=False)
        self.register[Modifier.CONTROL + Modifier.CONTROL + Gatename.NOT] = GateInfo(3, CGC().create(self.register[Gatename.NOT], [-2, -1]).matrix, GateSignature(Gatename.NOT, pre = Modifier.CONTROL + Modifier.CONTROL), offset = -2, multi=False)

    def get(self, request):
        if request.gate == Gatename.MEASUREMENT:
            return Gate(self._check_register(request.gate), request.qubit, request.gate)
        else:
            signature = GSC.encode(request)
            gateinfo = self._check_register(signature)
            if gateinfo is None:
                result = self._call_creator(request)
                if result is None:
                    return None
                gateinfo = self._add(request, result, signature)
            qubits = [request.qubit] if request.size == 1 else [request.qubit, request.qubit + request.size - 1]
            controls = [pre + qubits[0] for pre in request.controls[0]] + [post + qubits[-1] for post in request.controls[1]]
            return Gate(gateinfo, qubits, request.gate, controls)

    def _add(self, request, result, signature):
        gateinfo = GateInfo(result.size, result.matrix, signature, multi=result.multi, offset=result.offset)
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
        






