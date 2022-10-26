"""
modélisation du passage du courrant par un booléen
"""
import time
import flet
from flet import Page,Text,Row,Column,ElevatedButton,TextButton,TextField

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
    
class Nombre(Gate):
    def __init__(self,Nombre,est_binaire):
        self._longueur = self._calculLongueur(Nombre,est_binaire)
        if est_binaire:
            self.nombre = Nombre
        else:
            self.nombre = self._versBinaire(Nombre)
        self._est_binaire = True

    def __str__(self):
        return f"la valeur de l'instance est: {self.nombre}"

    def _calculLongueur(self,nombre,est_binaire):
        if est_binaire:#si il est binaire alors on renvoie la longueur de la string
            return len(nombre)
        else: #sinon on regarde la puissance de 2 la plus élevée du nombre
            l:int = 0
            nombre = int(nombre)
            while nombre-(2**l)>= nombre/2:
                l+=1
            l+=1
            return l

    def _versBinaire(self, nombre):
        binaire:str = ""
        for i in range(self._longueur):
            if nombre >= 2**(self._longueur-i-1):
                binaire+="1"
                nombre -=(2**(self._longueur-i-1))
            else:
                binaire+="0"
        return binaire
        
    def __add__(self, Nombre2):
        N1:str = "0"+str(self.nombre)#un 0 au début permet de palier les problèmes de dépassements si le nombre en binaire ne comporte que des bits True e.g:15(1111),7(111)
        N2:str = "0"+str(Nombre2.nombre)
        inter = (0,0)
        resultat = ""
        if Nombre2._longueur > self._longueur:
            longueurMax = Nombre2._longueur
            N1 = "0"*(longueurMax-self._longueur) + N1#ajoute un 0 au début du nombre le plus petit afin de qu'ils aient la même longueur
        else:
            longueurMax = self._longueur
            N2 = "0"*(longueurMax-Nombre2._longueur) + N2
        for i in range(self._longueur+1):
            P = Gate(int(N1[len(N1)-i-1]))#conversion en integer car la conversion d'une string en booleen renvoie False si la string est vide, True sinon. Or, ce n'est pas le comportement attendu dans ce cas de figure, la conversion en integer est donc nécessaire.
            Q = Gate(int(N2[len(N2)-i-1]))
            Cin = Gate(bool(int(inter[0])))
            inter = P.circuit_additionneur(Q,Cin)
            resultat = str(int(inter[1])) + resultat
        return Nombre(resultat, True)._versBase16(longueurMax+1)#incrémentation nécessaire afin de ne pas effectuer de dépassements


    def _versBase16(self,longueur):
        return int(str(self.nombre),2)#la méthode int() peut uniquement convertir des String en int, la type de self.nombre est un integer, il faut donc le convertir en string afin de le reconvertir en base 2
        base16 = 0
        for i in range(longueur):
            print(i,longueur,self.nombre[i])
            base16+= int(self.nombre[i])*2**(longueur-i-1)
        return base16
        """
        sinon, la méthode int() possède un argument optionnel permettant la conversion de son argument requis en base 16. Nous pouvons simplement écrire:
        
        """
    
    def stats(self, nombre2, iterations):
        t1= []
        t2= []
        for _ in range(iterations):
            dbt = time.perf_counter()
            self + nombre2
            t1.append(time.perf_counter() - dbt)
            N1,N2 = self.nombre,nombre2.nombre
            dbt2 = time.perf_counter()
            N1 + N2
            t2.append(time.perf_counter() - dbt2)
        m1=0
        m2=0
        for i in range(len(t1)):
            m1+= t1[i]
            m2 += t2[i]
        return m1/len(t1), m2/len(t2)




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

def main(page : Page):
    page.theme_mode = "light"
    def test(e):
        nombre1 = Nombre(int(entree1.value),False)
        nombre2 = Nombre(int(entree2.value),False)
        resultat.value=f"résultat= {nombre1+nombre2}"
        page.update()
    entree1 = TextField(hint_text="Nombre 1")
    entree2 = TextField(hint_text="Nombre 2")
    resultat = Text(value="")
    page.controls.append(Column(controls=[Row(controls=[entree1,entree2]),TextButton(text="addition",on_click=test),resultat]))
    page.update()


flet.app(target=main)