class Modifier(object):

    CONTROL = "ctrl"
    HERMITIAN = "*"

class Gatename(object):
    """description of class"""

    IDENTITY = "i"
    HADAMARD = "h"
    PAULI_X = "x"
    PAULI_Y = "y"
    PAULI_Z = "z"
    NOT = PAULI_X
    SWAP = "swap"
    T = "t"
    S = "s"
    T_HERMITIAN = T + Modifier.HERMITIAN
    S_HERMITIAN = S + Modifier.HERMITIAN


