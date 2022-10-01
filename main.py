"""
modélisation du passage de courrant par un booléen
"""

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
        if Gate(self.booleen)._logic_not().booleen:           
            if Gate(Q.booleen)._logic_not().booleen:
                return Gate(True)     
        return Gate(False)
        """
        équivalent à :
        return Gate(not self.booleen and not Q.booleen)
        """

    def _logic_and(self,Q):
        A = self._logic_nor(self)
        B = Q._logic_nor(Q)
        return Gate(A._logic_nor(B).booleen)

    def _logic_or(self,Q):
        A = self._logic_nand(self)
        B = Q._logic_nand(Q)
        return Gate(A._logic_nand(B).booleen)

    def _logic_xor(self,Q):
        A = self._logic_and(Q._logic_not())
        B = Q._logic_and(self._logic_not())
        return Gate(A._logic_or(B).booleen)

    def _logic_xnor(self,Q):
        return Gate(self._logic_xor(Q)._logic_not().booleen)

    def circuit_additionneur(self,Q,Cin):
        E1 = self._logic_xor(Q)
        S = E1._logic_xor(Cin).booleen
        E2 = E1._logic_and(Cin)
        E3 = self._logic_and(Q)
        Cout = E2._logic_or(E3).booleen
        return Cout, S
    
class Nombre(Gate):
    
    def __init__(self,Nombre,est_binaire):
        if est_binaire:
            self.nombre = Nombre
        else:
            self.nombre = self._versBinaire(Nombre)

    def _versBinaire(self, Nombre):
        binaire:str = ""
        for i in range(8):
            if Nombre >= 2**(8-i-1):
                binaire+="1"
                Nombre -=(2**(8-i-1))
            else:
                binaire+="0"
        return binaire

    def addition(self,Nombre2):
        N1 = self.nombre
        N2 = Nombre2.nombre
        N3 = "00000000"
        for i in range(8):
            N3[len(N3)-i-1] = Gate(bool(N1[len(N1)-i-1])).circuit_additionneur(Gate(bool(N2[len(N2)-i-1])),Gate(bool(N3[len(N3)-i-1])))
        return N3



P: Gate = Gate(True)
Q: Gate = Gate(False)
Cin: Gate = Gate(False)
#print(P._logic_not())
#print(P._logic_nand(Q))
#print(P._logic_nor(Q))
#print(P._logic_and(Q))
#print(P._logic_or(Q))
#print(P._logic_xor(Q))
#print(P._logic_xnor(Q))
#print(P.circuit_additionneur(Q, Cin))

N1: Nombre = Nombre(15,False)
N2: Nombre = Nombre("0010010",True)
print(N2.addition(N1))


 