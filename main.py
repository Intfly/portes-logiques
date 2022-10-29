import time
import flet
from nombre import *
from interface import *

"""
modelisation du passage du courrant par un booleen
"""


#               TESTS               #

P: Gate = Gate(True)
Q: Gate = Gate(False)
Cin: Gate = Gate(True)
#print(P._logic_not())
#print(P._logic_nand(Q))
#print(P._logic_nor(Q))
#print(P._logic_and(Q))
#print(P._logic_or(Q))
#print(P._logic_xor(Q))
#print(P._logic_xnor(Q))
#print(P.circuit_additionneur(Q, Cin))

N1: Nombre = Nombre("11",True)
N2: Nombre = Nombre("1111",True)
#print(N2 + N1)
#print(N2._versBase16())

R1: Nombre = Nombre(10,False)
R2: Nombre = Nombre(10,False)
#print(N1.stats(N2,100000))
#print(R1 + R2)
#print(N2._longueur)

#               INTERFACE               #

flet.app(target=main,assets_dir="assets")