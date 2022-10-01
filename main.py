"""
modélisation du passage de courrant par un booléen
"""

from tkinter import N


class Gate:
    def __init__(self,valeur_bouleenne: bool):
        self.booleen: bool = valeur_bouleenne
    
    def __str__(self):
        return f"valeur booléenne: {self.booleen}"

    def _logic_not(self):
        if self.booleen:
            return Gate(False)
        return Gate(True)
    
    def _logic_nand(self,Q):
        if self.booleen:
            if Q.booleen:
                return Gate(False)
        return Gate(True)
        """
        équivalent à:
        return Gate(self.booleen and Q.booleen)
        """

    def _logic_nor(self, Q):
        if Gate(self.booleen).logic_not().booleen:           
            if Gate(Q.booleen).logic_not().booleen:
                return Gate(True)     
        return Gate(False)
        """
        équivalent à :
        return Gate(not self.booleen and not Q.booleen)
        """

    def _logic_and(self,Q):
        A = self.logic_nor(self)
        B = Q.logic_nor(Q)
        return Gate(A.logic_nor(B).booleen)

    def _logic_or(self,Q):
        A = self.logic_nand(self)
        B = Q.logic_nand(Q)
        return Gate(A.logic_nand(B).booleen)

    def _logic_xor(self,Q):
        A = self.logic_and(Q.logic_not())
        B = Q.logic_and(self.logic_not())
        return Gate(A.logic_or(B).booleen)

    def _logic_xnor(self,Q):
        return Gate(self.logic_xor(Q).logic_not().booleen)

    def circuit_additionneur(self,Q,Cin):
        E1 = self.logic_xor(Q)
        S = E1.logic_xor(Cin).booleen
        E2 = E1.logic_and(Cin)
        E3 = self.logic_and(Q)
        Cout = E2.logic_or(E3).booleen
        return Cout, S
    
class Nombre(Gate):
    
    def __init__(self,Nombre):
        self.nombre = self._binaire(Nombre)

    def _binaire(self, Nombre):
        binaire :int =0
        while Nombre  > 0:
            n=0
            while 2**n < Nombre:
                n+=1
            Nombre -=(2**n)
            binaire += 1+(0*10**(n-1))
        return binaire

P = Gate(True)
Q = Gate(False)
Cin = Gate(False)
#print(P.logic_not())
#print(P.logic_nand(Q))
#print(P.logic_nor(Q))
#print(P.logic_and(Q))
#print(P.logic_or(Q))
#print(P.logic_xor(Q))
#print(P.logic_xnor(Q))
#print(P.circuit_additionneur(Q, Cin))

N1 = Nombre(5)
print(N1.nombre)


 