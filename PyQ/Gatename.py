class Modifier(object):

    CONTROL = "c"
    HERMITIAN = "*"

class Gatename(object):
    """description of class"""

    IDENTITY = "i"
    H = "h"
    X = "x"
    Y = "y"
    Z = "z"
    NOT = X
    SWAP = "swap"
    T = "t"
    S = "s"
    T_HERMITIAN = T + Modifier.HERMITIAN
    S_HERMITIAN = S + Modifier.HERMITIAN


