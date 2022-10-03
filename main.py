"""
modélisation du passage du courrant par un booléen
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

    def __str__(self):
        return f"la valeur vaut: {self.nombre}"

    def _versBinaire(self, Nombre):
        binaire:str = ""
        for i in range(8):
            if Nombre >= 2**(8-i-1):
                binaire+="1"
                Nombre -=(2**(8-i-1))
            else:
                binaire+="0"
        return binaire
        
    def __add__(self,Nombre2):
        N1 = self.nombre
        N2 = Nombre2.nombre
        inter = (0,0)
        resultat = ""
        for i in range(8):
            P = Gate(int(N1[len(N1)-i-1]))
            Q = Gate(int(N2[len(N2)-i-1]))
            Cin = Gate(bool(int(inter[0])))
            inter = P.circuit_additionneur(Q,Cin)
            resultat = str(int(inter[1])) + resultat
        return Nombre(resultat, True)._versBase16()

    def _versBase16(self):
        return int(self.nombre,2)
        print(self.nombre)
        base16 = 0
        for i in range(8):
            print(base16)
            base16+= (int(self.nombre[7-i])**7-i)
        return base16

import time

def stats(iter):
    t1= []
    t2= []
    for _ in range(iter):
        dbt = time.perf_counter()
        R1 + R2
        t1.append(time.perf_counter() - dbt)
        dbt2 = time.perf_counter()
        15+1
        t2.append(time.perf_counter() - dbt2)
    m1=0
    m2=0
    for i in range(len(t1)):
        m1+= t1[i]
        m2 += t2[i]
    return m1/len(t1)*10000, m2/len(t2)*10000

#               TESTS               #

P: Gate = Gate(True)
Q: Gate = Gate(True)
Cin: Gate = Gate(True)
#print(P._logic_not())
#print(P._logic_nand(Q))
#print(P._logic_nor(Q))
#print(P._logic_and(Q))
#print(P._logic_or(Q))
#print(P._logic_xor(Q))
#print(P._logic_xnor(Q))
#print(P.circuit_additionneur(Q, Cin))

N1: Nombre = Nombre("00000001",True)
N2: Nombre = Nombre("000001111",True)
#print(N2.addition(N1))
#print(N2._versBase16())

R1: Nombre = Nombre(15,False)
R2: Nombre = Nombre(1,False)

print(stats(2000))