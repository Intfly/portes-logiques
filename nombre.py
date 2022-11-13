from gate import *
import time

class Nombre:
    def __init__(self,Nombre,est_binaire):
        """
        Le constructeur de la classe prend en argument un nombre en base 10 sous la forme d’un int ou un nombre en base 2 sous la forme d’une string. 
        Il prend aussi une valeur booléenne est_binaire décrivant le premier argument. 
        Ce constructeur convertit en binaire le nombre s’il ne l’est pas.
        """
        assert type(Nombre) == int or type(Nombre) == str
        if type(Nombre) == int:
            assert Nombre >= 0
        assert type(est_binaire) == bool
        self._longueur = self._calculLongueur(Nombre,est_binaire)
        if est_binaire:
            self.nombre = Nombre
        else:
            self.nombre = self._versBinaire(Nombre)
        self._est_binaire = True

    def __str__(self):
        """
        renvoie une description de la valeur de l’instance
        """
        return f"la valeur de l'instance est: {self.nombre}"

    def _calculLongueur(self,nombre,est_binaire):
        """
        renvoie la longueur du nombre qu’il soit binaire ou non.
        nombre est un int ou une string et est_binaire est un booléen.
        """
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
        """
        convertit un nombre en binaire. 
        nombre est un int.
        """
        binaire:str = ""
        for i in range(self._longueur):
            if nombre >= 2**(self._longueur-i-1):
                binaire+="1"
                nombre -=(2**(self._longueur-i-1))
            else:
                binaire+="0"
        return binaire
        
    def __add__(self, Nombre2):
        assert type(Nombre2) == Nombre
        """
        renvoie la somme de deux instances de la classe Nombre sous la forme d’un entier. Et ce, grâce au circuit additionneur de la classe Gate. 
        Nombre2 est une instance de la classe Nombre."""
        N1:str = "0"+str(self.nombre)#un 0 à gauche permet de palier les problèmes de dépassements si le nombre en binaire ne comporte que des bits True e.g:15(1111),7(111)
        N2:str = "0"+str(Nombre2.nombre)
        inter = (0,0)
        resultat = ""
        if Nombre2._longueur > self._longueur:
            longueurMax = Nombre2._longueur
            N1 = "0"*(longueurMax-self._longueur) + N1#ajoute un 0 au début du nombre le plus petit afin de qu'ils aient la même longueur
        else:
            longueurMax = self._longueur
            N2 = "0"*(longueurMax-Nombre2._longueur) + N2
        for i in range(len(N1)):
            P = Gate(int(N1[len(N1)-i-1]))#conversion en integer car la conversion d'une string en booleen renvoie False si la string est vide, True sinon. Or, ce n'est pas le comportement attendu dans ce cas de figure, la conversion en integer est donc nécessaire.
            Q = Gate(int(N2[len(N2)-i-1]))
            Cin = Gate(bool(int(inter[0])))
            inter = P.circuit_additionneur(Q,Cin)
            resultat = str(int(inter[1])) + resultat
        return Nombre(resultat, True)._versBase10()#incrémentation nécessaire afin de ne pas effectuer de dépassements

    def _versBase10(self):
        """
        renvoie le nombre de l’instance en base10. 
        """
        return int(str(self.nombre),2)#la méthode int() peut uniquement convertir des String en int, la type de self.nombre est un integer, il faut donc le convertir en string afin de le reconvertir en base 2

    
    def stats(self, nombre2, iterations):
        """
        renvoie un tuple contentant le temps d'exection moyen de l'addition de deux instance de la classe nombre, une fois en utilisant la méthode __add__ et une fois en utilisant l'opérateur présent nativement dans python
        nombre2 est une instance de la classe nombre et intérations est in int donnant le nombre d'itérations de la boucle
        """
        assert type(iterations) == int
        assert iterations >0
        assert type(nombre2) == Nombre
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
        return m1/iterations, m2/iterations


