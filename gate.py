class Gate:
    def __init__(self,valeur_bouleenne: bool,operation = None, y=None):
        """
        Le constructeur de la classe prend en argument la valeur booléenne de l’instance, ainsi que deux arguments permettant de réaliser des opérations dès l’initialisation de l’instance.
        valeur_booleenne est une valeur booléenne, operation, une string et y un autre valeur booléenne.
        """
        self.booleen: bool = valeur_bouleenne
        if operation != None:
            G2 = Gate(y)
            ope={"not":self._logic_not(),"nand":self._logic_nand(G2),"nor":self._logic_nor(G2),"and":self._logic_and(G2),"or":self._logic_or(G2),"xor":self._logic_xor(G2),"xnor":self._logic_xnor(G2)}
            self.booleen= ope[operation].booleen

    
    def __str__(self):
        """
        renvoie une phrase détaillant la valeur booléenne de l’instance.
        """
        return f"valeur booléenne: {self.booleen}"

    def _logic_not(self):
        """
        renvoie une instance de la classe Gate ayant pour valeur booléenne l’inverse de celle de la première instance.
        """
        if self.booleen:
            return Gate(False)
        return Gate(True)
    
    def _logic_nand(self,Q):
        """
        renvoie l’inverse de l’intersection de self et Q sous la forme d’une instance de la classe Gate. 
        Q est une instance de la classe Gate.
        """
        assert type(Q) == Gate
        if self.booleen:
            if Q.booleen:
                return Gate(False)
        return Gate(True)
        """
        équivalent à:
        return Gate(self.booleen and Q.booleen)
        """
   
    def _logic_nor(self, Q):
        """
        renvoie l’inverse de l’union de self et Q sous la forme d’une instance de la classe Gate. 
        Q est une instance de la classe Gate.
        """
        assert type(Q) == Gate
        if self._logic_not().booleen:           
            if Q._logic_not().booleen:
                return Gate(True)     
        return Gate(False)
        """
        équivalent à :
        return Gate(not self.booleen and not Q.booleen)
        """
    

    def _logic_and(self,Q):
        """
        renvoie l’intersection de self et Q sous la forme d’une instance de la classe Gate. 
        Q est une instance de la classe Gate.
        """
        assert type(Q) == Gate
        A = self._logic_nor(self)
        B = Q._logic_nor(Q)
        return A._logic_nor(B)
    
    def _logic_or(self,Q):
        """
        renvoie l’union de self et Q sous la forme d’une instance de la classe Gate. 
        Q est une instance de la classe Gate.
        """
        assert type(Q) == Gate
        A = self._logic_nand(self)
        B = Q._logic_nand(Q)
        return A._logic_nand(B)

    def _logic_xor(self,Q):
        """
        renvoie l'union privée de la réunion de self et Q  sous la forme d’une instance de la classe Gate. 
        Q est une instance de la classe Gate.
        """
        assert type(Q) == Gate
        A = self._logic_and(Q._logic_not())
        B = Q._logic_and(self._logic_not())
        return A._logic_or(B)

    def _logic_xnor(self,Q):
        """
        renvoie l'inverse de l'union privée de la réunion de self et Q sous la forme d’une instance de la classe Gate. 
        Q est une instance de la classe Gate.
        """
        return self._logic_xor(Q)._logic_not()

    def circuit_additionneur(self,Q,Cin):
        """
        assert type(Q) == Gate
        renvoie un tuple contenant l’addition binaire de self, Q et Cin. 
        Q et Cin sont des instances de la classe Gate.
        """
        assert type(Q) == Gate
        E1 = self._logic_xor(Q)
        S = E1._logic_xor(Cin).booleen
        E2 = E1._logic_and(Cin)
        E3 = self._logic_and(Q)
        Cout = E2._logic_or(E3).booleen
        return Cout, S