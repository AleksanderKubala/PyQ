from PyQ.Circuit import Circuit
from PyQ.Gatename import Gatename
cir = Circuit(3)
changes = cir.add(Gatename.PAULI_X, 0, 0, 1)
changes = cir.add(Gatename.HADAMARD, 2, 0)
#changes = cir.remove((0,), 0)
print(cir.layers[0].gates[0])
print(cir.layers[0].gates[1])
print(cir.layers[0].gates[2])

