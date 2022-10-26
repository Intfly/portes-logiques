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
        if self._logic_not().booleen:           
            if Q._logic_not().booleen:
                return Gate(True)     
        return Gate(False)
        """
        équivalent à :
        return Gate(not self.booleen and not Q.booleen)
        """

    def _logic_and(self,Q):
        A = self._logic_nor(self)
        B = Q._logic_nor(Q)
        return A._logic_nor(B)

    def _logic_or(self,Q):
        A = self._logic_nand(self)
        B = Q._logic_nand(Q)
        return A._logic_nand(B)

    def _logic_xor(self,Q):
        A = self._logic_and(Q._logic_not())
        B = Q._logic_and(self._logic_not())
        return A._logic_or(B)

    def _logic_xnor(self,Q):
        return self._logic_xor(Q)._logic_not()

    def circuit_additionneur(self,Q,Cin):
        E1 = self._logic_xor(Q)
        S = E1._logic_xor(Cin).booleen
        E2 = E1._logic_and(Cin)
        E3 = self._logic_and(Q)
        Cout = E2._logic_or(E3).booleen
        return Cout, S