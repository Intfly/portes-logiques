import flet
import time

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

from flet import (ButtonStyle, Column, Container, IconButton, Image,
                  Page, Row, Text, TextButton, TextField, UserControl, View,
                  alignment, margin, padding,GridView)
from flet.buttons import RoundedRectangleBorder
from nombre import *

#Les Container peuvent-être assimilées à des divs en HTML.
#Quant aux Column et Row, celles-ci permettent de d'ajouter respectivement des éléments sur le plan vertical et horizontal.
#En combinant ces trois éléments, nous pouvons réaliser des interfaces complètes.

def main(page : Page): # page est une instace de la classe Page
    page.window_width = 703#largeur en pixel de la page
    page.window_height = 550
    page.theme_mode = "light" # force le thème clair même l'OS est en thème sombre
    def route_change(route):
        """
        fonction permettant de changer de vue 
        route est une string contenant le nom de la vue à ajouter
        """
        page.views.clear()#supprime les vues
        page.views.append(#ajoute une vue, par défaut j'ajoute la vue du menu
            View(
                "/",
                [
                    Column(
                        controls=[
                            Container(content=Row(
                                controls=[
                                    TextButton("introduction", on_click=lambda _: page.go("/introduction")),# permet de changer de page
                                    TextButton("application", on_click=lambda _: page.go("/application1")),# permet de changer de page
                                ],
                                alignment = "end"# met les boutons à la fin de la row et non au début
                            ),padding=padding.only(top=10,right=10)),
                            Container(content=Text(value="algorithmie booléenne et son application au sein des ordinateurs",size = 30,),margin=margin.only(top=110),padding=padding.only(left=5,right=100)),
                            Container(
                                content=TextButton(
                                    "calculatrice",
                                    style = ButtonStyle(
                                        bgcolor="#3283FD",
                                        color="#FFFFFF",
                                        padding=padding.symmetric(vertical=13,horizontal=40)),
                                    on_click=lambda _: page.go("/calculatrice")), # permet de changer de page
                                padding=padding.only(left=5)
                                ),
                            Container(content=Image(src="\img_menu.png"),margin=margin.only(left=250),width=430)
                        ]
                    )
                ],
                padding=padding.only(left=10),
            )
        )
        if page.route =="/introduction" or page.route in ["not","or","and","xnor","xor","nor","nand"]: #change la vue vers soit le menu ou soit la page de la porte logique désirée

            def click_bouton(e):
                page.views.append(View(e.control.data,[
                    Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/introduction")),padding=padding.only(left=10,top=10)),
                    ]))

            def bouton(nom):
                return TextButton(
                    content=Container(
                        content=Row(controls=[
                        Image(src=f"\calc\{nom}.png"),
                        Text(f"{nom}",size=25)],
                        alignment="spaceAround"),width=175,height=80,padding=padding.symmetric(horizontal=10,vertical=7),alignment=alignment.center,border_radius=10),
                    style=ButtonStyle(bgcolor="#10000000",color="#FF000000",overlay_color="#00000000",shape=RoundedRectangleBorder(radius=10)),
                    data=nom,#attribut invisible du bouton. Il sera utile par la suite
                    on_click=lambda _:page.go(nom))

            if page.route == "/introduction":
                page.views.append(View("/introduction",[
                    Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/")),padding=padding.only(left=10,top=10)),
                    Container(
                        content=Row(controls=[bouton("and"),bouton("or"),bouton("nand"),bouton("nor"),bouton("xnor"),bouton("xor"),bouton("not")],wrap=True,spacing=27,run_spacing=20,alignment="center"),
                        padding=padding.symmetric(horizontal=20,vertical=30)
                        )]))
            else:
                operateur_data={"not":{"description":"renvoie l'inverse d'un élément","symbole":u"A\u0305","symbole_maths":"¬A","symbole_elec":f"\introduction\{page.route}.png","table_verite":f"\introduction\{page.route}_tv.png"},
                                "and":{"description":"renvoie l'intersection de deux éléments","symbole":"A·B","symbole_maths":"A∧B","symbole_elec":f"\introduction\{page.route}.png","table_verite":f"\introduction\{page.route}_tv.png"}, 
                                "or":{"description":"renvoie l'union de deux éléments","symbole":"A+B","symbole_maths":u"A\u2228B","symbole_elec":f"\introduction\{page.route}.png","table_verite":f"\introduction\{page.route}_tv.png"},
                                "nand":{"description":"renvoie l'inverse de l'intersection de deux éléments","symbole":u"A\u0305·\u0305B\u0305","symbole_maths":"¬(A∧B)","symbole_elec":f"\introduction\{page.route}.png","table_verite":f"\introduction\{page.route}_tv.png"},
                                "nor":{"description":"renvoie l'inverse de l'union de deux éléments","symbole":u"A\u0305+\u0305B\u0305","symbole_maths":u"¬(A\u2228B)","symbole_elec":f"\introduction\{page.route}.png","table_verite":f"\introduction\{page.route}_tv.png"},
                                "xor":{"description":"renvoie l'union privée de l'intersection de deux éléments","symbole":"A⊕B","symbole_maths":u"A\u2262B","symbole_elec":f"\introduction\{page.route}.png","table_verite":f"\introduction\{page.route}_tv.png"},
                                "xnor":{"description":"renvoie l'inverse de l'union privée de l'intersection de deux éléments","symbole":"A\⊙B","symbole_maths":u"A\u2261B","symbole_elec":f"\introduction\{page.route}.png","table_verite":f"\introduction\{page.route}_tv.png"},
                                }
                description= "description"
                symbole= "symbole"
                symbole_elec= "symbole_elec"
                table_verite= "table_verite"
                symbole_maths= "symbole_maths"
                page.views.append(View(page.route,[
                    Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/introduction")),padding=padding.only(left=10,top=10)),
                    Container(content=Column(controls=[
                        Text(f"{page.route}:",size=30),
                        Text(f"description:\n    {operateur_data[page.route][description]}\n\nsymbole algébrique et mathématique:\n      {operateur_data[page.route][symbole]}   {operateur_data[page.route][symbole_maths]}\n\nsymbole et table de vérité:",size=20),
                        Container(content=Row(controls=[Image(src=operateur_data[page.route][symbole_elec],height=70),Image(src=operateur_data[page.route][table_verite],height=150)],alignment="spaceBetween"),padding=padding.only(left=10),width=400)
                    ]),padding=padding.only(left=30)),
                    ]))


        if page.route == "/application1":
            resultat_addition = Text(value="",size=18)
            def addition(e):# on peut assimiler e au context.
                if entree1.value != ""and entree2.value != "":
                    nombre1 = Nombre(int(entree1.value),False)
                    nombre2 = Nombre(int(entree2.value),False)
                    resultat_addition.value=f"résultat= {nombre1+nombre2}"
                    page.update()#met à jour la page
            entree1 = TextField(hint_text="Nombre 1",label="Nombre 1",on_change=addition, width=100,height=50)# permet d'entrer du texte
            entree2 = TextField(hint_text="Nombre 2",label="Nombre 2",on_change=addition,width=100,height=50)
            
            
            page.views.append(
                View(
                    "/application1",
                    [
                        Column(controls=[
                            Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/")),padding=padding.only(left=0,top=10)),
                            Text("les portes logiques ont un rôle crucial au sein des ordinateurs, elles permettent notamment de réaliser des additions binaires.\nEntrez des nombres dans les cases suivantes.",size=18),
                            Row(controls=[entree1,entree2]),
                            resultat_addition,
                            Text("Cette addition a justement été réalisée grâce à des portes logiques. Pour cela, le programme suit le circuit suivant:",size=18),
                            Row(controls=[Image(src="\.application\_full_adder.png",height=150),
                            Container(content=TextButton(content=Text("suivant",size=20), style=ButtonStyle(color="#FAFFFFFF",overlay_color="#AA000000",bgcolor="#3283FD"),width=160,height=50,on_click= lambda _: page.go("/application2")),margin=margin.only(top=110,left=200))])
                        ]),
                    ],padding=padding.symmetric(horizontal=40)
                )
            )
        if page.route == "/application2":
            page.views.append(View("/application2",[Column(controls=[
                Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/application1")),padding=padding.only(left=0,top=10)),
                Text("utiliser des portes logiques afin de réaliser des additions est en plus lent que de simplement utiliser l'opérateur présent nativement dans python. En Effet, le l'utilisation de portes logiques rend le calcul 350x plus lent.\n\nIl est par ailleurs possible de réduire le temps d'exécution en utilisant un langage plus bas niveau. En transposant le code en C++, Le temps d'exécution a été réduit pas 3.",size=18),
                Container(Row(controls=[Image(src="\.application\logo_python.png",height=150),Image(src="\.application\logo_cpp.png",height=150)],alignment="spaceAround"),margin=margin.only(top=35))
            ])],padding=padding.symmetric(horizontal=40)))
        
        if page.route == "/calculatrice":#vue sous la forme d'une classe
            class calculatrice(UserControl):# la class UserControl permet de construire des composants réutilisables
                def __init__(self):
                    self.resultat= Text(value="out= A+B",size=30)
                    self.calcul= ""
                    self.ope = [""]
                    self.ouverte= 0
                    self.tableau_boutons= Row(controls=[self.gate("not",True,False),self.gate("or",True,False),self.gate("and",True,False),self.gate("A",False,True),self.gate("B",False,True),self.gate("C",False,True),self.gate("xnor",True,False),self.gate("xor",True,False),self.gate("nor",True,False),self.gate("nand",True,False),self.gate("(",False,True),self.gate(")",False,True)],wrap=True,spacing=37,run_spacing=14)
                
                def action_boutons(self,e,maths=False):     
                    """
                    réalise l'action du bouton sur lequel l'utilisateur a cliqué.
                    e désigne le contexte d'activation du bouton
                    maths est un booléen permettant de déterminer si les symboles algébriques ou mathématiques devront être ajoutés.
                    """             
                    if maths: #définit le placement des syboles entre eux.
                        if len(self.ope) == 1:
                            self.resultat.value = "out= "
                        equivalence= {"not":u"\u00ac","and":u"\u22c0","or":u"\u22c1","xor":u"\u2262","xnor":u"\u2261","nand":u"\u00ac(x\u22c0y)","nor":u"\u00ac(x\u22c1y)"}
                        if e.data in ["A","B","C"]:
                            self.resultat.value += e.data
                        elif e.data in ["and","or","xor","xnor"]:
                            self.resultat.value += equivalence[e.data]
                        elif e.data in ["(",")"]:
                            if len(self.ope)>=3 and self.ope[-2] in ["nand","nor"] or self.ope[-3] in ["nand","nor"]:
                                self.resultat.value+=")"
                            elif self.ouverte == 0 and e.data == ")":
                                self.resultat.value = "out= ("+self.resultat.value[5:]+")"
                            elif e.data == "(":
                                self.ouverte -=1
                                self.resultat.value+= "("
                            elif e.data == ")":
                                self.ouverte +=1
                                self.resultat.value += ")"
                        elif e.data  == "not":
                            if self.ope[-1] in ["A","B","C"]:
                                self.resultat.value = self.resultat.value[:-1] + equivalence["not"] + self.resultat.value[-1]
                            elif self.ope[-1] == ")":
                                derniere_parenthese_ouvrante=0
                                compteur=0
                                for i in range(len(self.resultat.value)-2,4,-1):
                                    if self.resultat.value[i]=="(" and compteur == 0: 
                                        derniere_parenthese_ouvrante = i
                                        break
                                    if self.resultat.value[i]==")":
                                        compteur+=1
                                    elif self.resultat.value[i]=="(":
                                        compteur-=1
                                self.resultat.value = self.resultat.value[:derniere_parenthese_ouvrante:] + equivalence["not"] +self.resultat.value[derniere_parenthese_ouvrante:]
                        elif e.data in ["nor","nand"]:
                            if self.ope[-1] == "not":
                                self.resultat.value = self.resultat.value[:-2] + equivalence["not"] + "(" + self.resultat.value[-2:] + equivalence[e.data[1:]]
                            if self.ope[-1] in ["A","B","C"]:
                                self.resultat.value = self.resultat.value[:-1] + equivalence["not"] + "(" + self.resultat.value[-1:] + equivalence[e.data[1:]]

                        self.ope.append(e.data)
                          
                    else:
                        operations=["not","or","and","xnor","xor","nor","nand"]
                        if len(self.ope)==1: self.resultat.value ="out= "#permet d'enlever le A and B par défaut. Il y a déjà un élement dans self.ope donc on compare la longueur avec 1
                        for i in range(len(operations)):#le but ici est d'itérer parmi les boutons possibles et de changer l'affichage en conséquence
                            if e.control.data == operations[i]:
                                if self.ope[-1] in operations[1:]+["("] or e.control.data==self.ope[-1]:#permet d'empécher que deux signes se suivent sans lettre intermédiaire
                                    break
                                operations_calcul=[u"\u0305","+","·","⊙","⊕"]#0305 correspond au code Unicode de la barre horizontale sur un élément.
                                
                                #les lignes suivantes décrivent le cas où le not doit être distribué sur l'ensemble de la parenthèse
                                if e.control.data == "not" and self.ope[-1] in ["(",")"]:
                                    inter= ""#l'assignation par index n'est pas possible pour les strings, il faut donc créer une variable intermédiaire pour contenir les nouveaux élements.
                                    morgan= False
                                    morgan_override = True
                                    compteur= 0
                                    derniere_parenthese_ouvrante=0
                                    for i in range(len(self.resultat.value)-2,4,-1):
                                        if self.resultat.value[i]=="(" and compteur == 0: 
                                            derniere_parenthese_ouvrante = i
                                            break
                                        if self.resultat.value[i]==")":
                                            compteur+=1
                                            morgan_override = False
                                        elif self.resultat.value[i]=="(":
                                            compteur-=1                                              
                                    for i in range(derniere_parenthese_ouvrante,len(self.resultat.value)):
                                        #nous devons traiter le cas où l'expression correspond à une des loi de morgan, auquel cas nous pouvons simplifier l'expression
                                        #nous vérifions donc si l'une des lois de morgan est verifiée par disjonction des cas.
                                        if self.resultat.value[i]=="(" and self.resultat.value[i+1] in ["A","B","C"] :
                                            if self.resultat.value[i+2]==u"\u0305" and self.resultat.value[i+3]in["+","·"] and self.resultat.value[i+4] in ["A","B","C"]:
                                                if self.resultat.value[i+5]==u"\u0305" and self.resultat.value[i+6]==")":
                                                    morgan=True
                                                elif self.resultat.value[i+5] ==")":
                                                    morgan=True
                                            if self.resultat.value[i+2]in["+","·"] and self.resultat.value[i+3] in ["A","B","C"]:
                                                if self.resultat.value[i+4]==u"\u0305" and self.resultat.value [i+5]==")" and len(self.resultat.value)==i+6:
                                                    morgan= True
                                                elif self.resultat.value [i+4]==")" :
                                                    morgan = True
                                        if morgan and morgan_override:
                                            if self.resultat.value[i]==u"\u0305":
                                                inter = inter[:-1]
                                            elif self.resultat.value[i] in ["+","·"]:
                                                dico_morgan={"+":"·","·":"+"}
                                                inter += f'{dico_morgan[self.resultat.value[i]]}'
                                            elif self.resultat.value[i] in ["A","B","C"]:
                                                inter+=f"{self.resultat.value[i]}{operations_calcul[0]}"
                                            elif self.resultat.value[i] in ["(",")"]:
                                                inter+=f"{self.resultat.value[i]}"
                                        #cette instruction conditionelle est exécutée lorsque les lois de Morgan ne sont pas respectées
                                        else:
                                            inter = f"{inter}{self.resultat.value[i]}{operations_calcul[0]}"#cas géneral
                                            if self.resultat.value[i] == u"\u0305":
                                                inter = inter[:-1]#la ligne deux ligne au dessus rajoute deux barre, on en enlève donc 1.
                                        if self.resultat.value[i] == ")":morgan = False#remet la valeur booléenne à son état initial après la parenthèse
                                    self.resultat.value = f"out= {self.resultat.value[5:derniere_parenthese_ouvrante]}{inter}"
                                    self.ope.append(e.control.data)

                                elif e.control.data in ["nand","nor"]:
                                    if e.control.data == "nand":
                                        self.resultat.value=f"out= {self.resultat.value[5:]}{operations_calcul[0]}·{operations_calcul[0]} {operations_calcul[0]}"
                                        self.ope.append(e.control.data)
                                    else:
                                        self.resultat.value=f"out= {self.resultat.value[5:]}{operations_calcul[0]}+{operations_calcul[0]} {operations_calcul[0]}"
                                        self.ope.append(e.control.data)
                                        
                                #les lignes suivantes décrivent le cas où le bouton a un symbole différent de not,nor et nand.
                                else:
                                    if len(self.ope)==1: self.resultat.value ="out= A"#place automatiquement la lettre A
                                    self.resultat.value=f"out= {self.resultat.value[5:]}{operations_calcul[i]}"#[5:]permet d'enlever le "out=" dans la valeur du texte affiché.
                                    self.ope.append(e.control.data)
                                break

                            #les lignes suivantes décrivent le cas où le bouton a une parenthèse pour data
                            elif e.control.data in ["(",")"]:
                                if  (e.control.data == "("and self.ope[-1] in ["A","B","C","not"]) or (e.control.data == ")"and self.ope[-1] in operations[1:]) or (self.ope[-1]=="not"and self.ope[-2]==")") or (len(self.ope)==1):#empêche les erreurs d'inattention
                                    break
                                if e.control.data == "(":
                                    self.ouverte+= 1
                                    self.resultat.value=f"out= {self.resultat.value[5:]}("
                                    self.ope.append(e.control.data)
                                elif e.control.data ==")" and self.ouverte >0:
                                    self.resultat.value=f"out= {self.resultat.value[5:]})"
                                    self.ouverte-= 1
                                    self.ope.append(e.control.data)
                                else:
                                    self.resultat.value=f"out= ({self.resultat.value[5:]})"
                                    self.ope.append(e.control.data)
                                break

                            #les lignes suivantes décrivent le cas où le bouton a une lettre pour data
                            elif e.control.data in ["A","B","C"]:
                                if self.ope[-1] in ["A","B","C","not",")"]:#permet d'empécher que deux lettres se suivent sans signe intermédiaire.
                                    break
                                if self.ope[-1] in ["nor","nand"]:
                                    self.resultat.value = self.resultat.value[:-2]+e.control.data+u"\u0305"
                                    self.ope.append(e.control.data)
                                else:
                                    self.resultat.value = f"out= {self.resultat.value[5:]}{e.control.data}"
                                    self.ope.append(e.control.data)
                                break
                                

                    print("\n")
                    page.update()

                def gate(self,nom,etat,texte,math=0):
                    """
                    méthode renvoyant un bouton correspondant aux paramètres
                    Il contient soit un texte, soit une image.
                    Il peut contenir le symbole mathématique ou algébrique.
                    """
                    if math:
                        equivalent= {"not":u"\u00ac","and":u"\u22c0","or":u"\u22c1","xor":u"\u2262","xnor":u"\u2261","nand":u"\u00ac(x\u22c0y)","nor":u"\u00ac(x\u22c1y)","A":"A","B":"B","C":"C","(":"(",")":")"}
                        if nom in ["nor","nand"]:
                            x= TextButton(
                            content=Container(content=Text(value=equivalent[nom],size=19),width=67,height=90,bgcolor="#10000000",border_radius=10,padding=padding.symmetric(horizontal=2),alignment=alignment.center),
                            on_click=lambda _: self.action_boutons(x,True),
                            style=ButtonStyle(padding=padding.only(),color="#DA000000",overlay_color="#00000000"),
                            data=nom)
                            return x
                        x= TextButton(
                            content=Container(content=Text(value=equivalent[nom],size=40),width=67,height=90,bgcolor="#10000000",border_radius=10,padding=padding.symmetric(horizontal=10),alignment=alignment.center),
                            on_click=lambda _: self.action_boutons(x,True),
                            style=ButtonStyle(padding=padding.only(),color="#DA000000",overlay_color="#00000000"),
                            data=nom)
                        return x
                    if etat:
                        return TextButton(
                            content=Container(content=Image(src=f"\calc\{nom}.png"),width=67,height=90,bgcolor="#10000000",border_radius=10,padding=padding.symmetric(horizontal=10),alignment=alignment.center),
                            on_click=self.action_boutons,
                            style=ButtonStyle(padding=padding.only(),overlay_color="#00000000"),
                            data=nom)
                    if texte:
                        return TextButton(
                            content=Container(content=Text(value=nom,size=40),width=67,height=90,bgcolor="#10000000",border_radius=10,padding=padding.symmetric(horizontal=10),alignment=alignment.center),
                            on_click=self.action_boutons,
                            style=ButtonStyle(padding=padding.only(),color="#DA000000",overlay_color="#00000000"),
                            data=nom)
                    return Text(value=f"{nom}2")


                def changer_mode(self,e):
                    """
                    méthode permettant de passer du mode algébrique au mode mathématique.
                    """
                    if e.selected:
                        pass#j'ai décidé de ne pas permettre à l'utilisateur de revenir au mode algébrique.Si nous voulions rendre cette option possible, nous pourrions créer des boutons avec les valeurs de self.ope et simuler leur click.
                    else:
                        equivalent= {"not":u"\u00ac","and":u"\u22c0","or":u"\u22c1","xor":u"\u2262","xnor":u"\u2261","nand":u"\u00ac(x\u22c0y)","nor":u"\u00ac(x\u22c1y)","A":"A","B":"B","C":"C","(":"(",")":")"}
                        e.tooltip= "représentation mathématique"
                        e.content.src= "\calc\_and_math.png"
                        nouveau= ""
                        for i in range(len(self.ope)):
                            if self.ope[i] == "not" and self.ope[i-1]==")":
                                compteur=0
                                for y in range(len(nouveau)-2,0,-1):
                                    if nouveau[y] == "(" and compteur == 0:
                                        nouveau = nouveau[:y]+equivalent["not"]+nouveau[y:]
                                    if nouveau[y]== "(":
                                        compteur-= 1
                                    elif nouveau[y]== ")":
                                        compteur+= 1
                                        
                            elif self.ope[i-1] in ["nor","nand"]:
                                nouveau += self.ope[i]+")"
                            elif self.ope[i] in ["or","and","xnor","xor"]:
                                nouveau+= equivalent[self.ope[i]]
                            elif self.ope[i] in ["nor","nand"]:
                                if len(self.ope)-1>=i+2:
                                    if self.ope[i-1]=="not" and self.ope[i+2]=="not":
                                        indice = len(nouveau)-3
                                    elif self.ope[i-1]=="not" or self.ope[i+2]=="not":
                                        indice = len(nouveau)-2
                                else:
                                    indice=len(nouveau)-1
                                nouveau = nouveau[:indice]+equivalent["not"]+"("+nouveau[indice:]+equivalent[self.ope[i][1:]]
                            elif self.ope[i] == "not":
                                if self.ope[i-2] in ["nor","nand"]:
                                    nouveau = nouveau[:-2]+equivalent["not"]+nouveau[-2:]
                                else:
                                    nouveau = nouveau[:-1]+equivalent["not"]+nouveau[-1]
                            else:
                                nouveau+= self.ope[i]
                        self.resultat.value= "out= "+nouveau
                        tableau= [("not",False,False,True),("or",False,True,True),("and",False,True,True),("A",False,True,True),("B",False,True,True),("C",False,True,True),("xnor",False,True,True),("xor",False,True,True),("nor",False,True,True),("nand",False,True,True),("(",False,True,True),(")",False,True,True)]
                        self.tableau_boutons.controls= [self.gate(tableau[i][0],tableau[i][1],tableau[i][2],tableau[i][3]) for i in range(len(tableau))]
                    e.selected= False
                    page.update()

                def ac(self,e):
                    """
                    remet l'expresion par défaut et supprime les actions des boutons
                    """
                    self.resultat.value= "out= A+B"
                    self.ope= [""]
                    page.update()

                def calculer(self):
                    """
                    rend le résultat accesible dans l'ensemble du programme et change la vue vers celle du résultat
                    """
                    global resultat_operation
                    resultat_operation= self.ope
                    page.route = "/calculatrice2"
                    page.update()

                def calc(self):
                    """
                    renvoie une vue contenant l'interface
                    """
                    bouton_mode =IconButton(content=Image(src="\calc\_algebre.png",height=30,width=30), style=ButtonStyle(bgcolor="#10000000"), selected=False, on_click=lambda _ : self.changer_mode(bouton_mode),tooltip="représentation algébrique")
                    return View("/calculatrice",
                        [
                            Column(controls=[
                            Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/")),padding=padding.only(left=10,top=10)),
                            Container(content=self.resultat,margin=margin.only(top=30,left=20,bottom=40,right=10)),
                            Container(height=1.5,width=700,bgcolor="#78000000"),
                            Row(controls=[
                                Container(content=Text("mode:"),margin=margin.only(left=30)),
                                bouton_mode,
                                TextButton("AC",
                                    style = ButtonStyle(
                                        bgcolor="#3283FD",
                                        color="#FFFFFF",
                                        padding=padding.symmetric(vertical=3,horizontal=20)),
                                    on_click=self.ac),
                                Container(TextButton("calculer",
                                    style = ButtonStyle(
                                        bgcolor="#3283FD",
                                        color="#FFFFFF",
                                        padding=padding.symmetric(vertical=3,horizontal=20)),
                                    on_click=lambda _: self.calculer()),
                                    margin=margin.only(left=375))
                                ],),
                            Container(height=1.5,width=700,bgcolor="#78000000"),
                            Container(content=self.tableau_boutons,padding=padding.symmetric(horizontal=50,vertical=20))
                    ])],padding=padding.only())

            page.views.append(calculatrice().calc())
            


        if page.route == "/calculatrice2":
            class Resultat:
                def __init__(self):
                    self.grid = GridView(
                        runs_count=5,
                        horizontal= True,
                        run_spacing=0,
                        spacing=0,
                        controls=[]
                    )
                    self.colonnes = int("A" in resultat_operation)+int("B" in resultat_operation)+int("C" in resultat_operation)
                    self.valeur_colonnes = ((1,0),((1,0,1,0),(1,0,0,1)),((1,0,1,0,1,0,1,0),(1,0,0,1,1,0,0,1),(1,1,1,1,0,0,0,0)))#tuple de tuple contentant les différentes valeurs possible de A,B et C
                    self.lettres = ["A","B","C"]
                    self.c=list(resultat_operation[1:])#copie du résultat sans le premier élément qui est une string vide
                    self.liste_calculs = []

                def texte(self,nom):
                    """
                    méthode renvoyant du texte avec une taille formalisée.
                    nom est une string
                    """
                    return Text(nom,size=25)
                
                def creation_grille(self):#création de la grille 
                    """
                    construit les fondations de la grille
                    """
                    if self.colonnes == 1:#ces trois instructions conditionelles me permetttent de créer les colonnes en fonction des valeurs d'entrée(en fonction des lettres et de leur nombre)
                        for i in self.lettres:
                            if i in resultat_operation:
                                self.grid.controls = self.texte(i),self.texte("1"),self.texte("0")
                        self.grid.runs_count=3
                    elif self.colonnes == 2:
                        mis = []#permet de savoir quel couple de lettre a été choisi e.g. ["A","C"],["B","C"],["A","B"]
                        for i in range(len(self.lettres)):
                            if self.lettres[i] in resultat_operation and self.lettres[i] not in mis:
                                if len(mis)<1:
                                    self.grid.controls += [self.texte(self.lettres[i])]+[self.texte(self.valeur_colonnes[1][0][y]) for y in range(4)]
                                    mis.append(self.lettres[i])
                                else:
                                    self.grid.controls += [self.texte(self.lettres[i])]+[self.texte(self.valeur_colonnes[1][1][y]) for y in range(4)]
                                    mis.append(self.lettres[i])
                    elif self.colonnes == 3:
                        self.grid.controls = [self.texte("A")]+[self.texte(self.valeur_colonnes[2][0][i]) for i in range(8)]+[self.texte("B")]+[self.texte(self.valeur_colonnes[2][1][i]) for i in range(8)]+[self.texte("C")]+[self.texte(self.valeur_colonnes[2][2][i]) for i in range(8)]
                        self.grid.runs_count=9
                    self.grid.controls += (self.texte("out"),)
            
                def calcul(self,copie):
                    """
                    renvoie un tableau avec les différentes valeurs possibles de l'expression en paramètre.
                    copie est un tableau contenant 4 copies de la même expression.
                    """
                    dico={1:1,0:0}
                    copie2= list(copie[1])       
                    valeurs_interm=[]
                    for v in range(2**self.colonnes):
                        print(copie[v])
                        if self.colonnes == 1:
                            x=self.valeur_colonnes[self.colonnes-1][v]
                        elif self.colonnes == 2:
                            x=self.valeur_colonnes[self.colonnes-1][0][v]
                            y=self.valeur_colonnes[self.colonnes-1][1][v]
                        elif self.colonnes == 3:
                            x=self.valeur_colonnes[self.colonnes-1][0][v]
                            y=self.valeur_colonnes[self.colonnes-1][1][v]
                            z=self.valeur_colonnes[self.colonnes-1][2][v]

                        if self.colonnes == 1:
                            dico = {"A":x,0:0,1:1}
                        elif self.colonnes == 2:
                            dico = {"A":x,"B":y,0:0,1:1}
                        elif self.colonnes == 3:
                            dico = {"A":x,"B":y,"C":z,0:0,1:1}

                        for i in range(len(copie[v])):
                            #print(f"passage {v} {i}")
                            #print(copie[v])
                            if copie[v][i] in ["A","B","C"]: #comportement si l'élément est une lettre
                                copie[v][i] = dico[copie[v][i]]
                                #print(copie[v])

                            elif copie[v][i] == "not": # comportement si l'élément est la porte "not", autrement dit, une porte à un seul élément
                                copie[v][i] = Gate(copie[v][i-1],"not").booleen 

                            elif copie[v][i] in ["or","and","nand","nor","xor","xnor"]: # comportement si l'élément est une porte à plusieurs éléments
                                if self.colonnes == 1:
                                    copie[v][i] = Gate(copie[v][i-1],copie[v][i],x).booleen

                                if self.colonnes in [2,3]:
                                    if len(copie[v])-1 >= i+2 and copie[v][i+2]=="not":  # executé lorsque la valeur à droite est le complément d'une valeur
                                        suivante =  Gate(dico[copie[v][i+1]],"not").booleen
                                        copie[v][i] = Gate(copie[v][i-1],copie[v][i],suivante).booleen

                                    elif i-2>0:
                                            copie[v][i] = Gate(copie[v][i-2],copie[v][i],dico[copie[v][i+1]]).booleen # prends le résultat de la dernière opération

                                    else:
                                        copie[v][i] = Gate(copie[v][i-1],copie[v][i],dico[copie[v][i+1]]).booleen #cas général

                        #print(copie)
                        if self.colonnes == 1:                        
                                valeurs_interm.append(int(copie[v][len(copie[v])-2]))
                        if self.colonnes in [2,3]:
                            if copie2[-1] in ["not",")"]:
                                valeurs_interm.append(int(copie[v][len(copie[v])-3]))
                            else:
                                valeurs_interm.append(int(copie[v][len(copie[v])-2]))
                    return valeurs_interm


            

                def indices_parenthese(self):
                    """
                    renvoie les indices des parenthèses sous la forme d'un tableau de tableau
                    """
                    self.creation_grille()
                    ouverte = 0
                    for i in range(len(self.c)):#renvoie les indices des différentes parenthèses de la boucle
                        if self.c[i] =="(":
                            ouverte += 1
                            self.liste_calculs.append([i+1,None])
                        elif self.c[i] ==")" and ouverte ==0:
                            if i != len(self.c)-1:
                                self.liste_calculs.append([0,i-1])
                        elif self.c[i] == ")":
                            ouverte -=1
                            for y in range(len(self.liste_calculs)):
                                if self.liste_calculs[y][1] == None:
                                    self.liste_calculs[y][1] = i
            
            
                def calcul_final(self):
                    self.indices_parenthese()
                    copie2 = []
                    resultat_final = []
                    if len(self.liste_calculs) == 0:#cas où il n'y a pas de parenthèses
                        for _ in range(2**self.colonnes):
                            copie2.append(list(self.c))
                        resultat_final = self.calcul(copie2)
                        for i in resultat_final:
                            self.grid.controls += (self.texte(i),)
        
                    else:#dans le cas où il y en a
                        #print(c,liste_calculs)
                        for i in range(len(self.liste_calculs)):#calcul des parenthèses
                            if i>0:
                                copie2=self.c[self.liste_calculs[i][0]:self.liste_calculs[i][1]]
                            else:# on regarde le cas où la parenthèse est au 1er indice, en effet, il suffit d'une seule parenthèse pour encadrer l'ensemble de l'expression. Sinon, il en faut deux. Les expressions ne sont donc pas identiques.
                                copie2=self.c[self.liste_calculs[i][0]:self.liste_calculs[i][1]+1]
                            #print(f"&&&&&&&&&&&&&&&&&&&& copie2 = {copie2} et bornes = {self.liste_calculs[i][0]}a{self.liste_calculs[i][1]}")
                            liste=[list(copie2) for _ in range(2**self.colonnes)]
                            resultat_final.append(self.calcul(liste))
        
        
                        compteur= 0
                        nombre_indice_a_retirer= 0
                        out=[]
                        for i in range(len(self.c)):#remplacement des parenthèses par "x" suivi de l'indice de la parenthèse dans le tableau liste_calculs
                            print(f"liste_calculs = {self.liste_calculs} et resultat_final= {resultat_final} i={i} c={self.c} compteur={compteur}")
                            if i == self.liste_calculs[compteur][0]:
                                if i==0:
                                    self.c= [("x",compteur)] + self.c[self.liste_calculs[compteur][1]+2-nombre_indice_a_retirer:]#+1 pour le dernier elem et +1 pour enlever la parenthèse
                                    nombre_indice_a_retirer+= self.liste_calculs[compteur][1]-self.liste_calculs[compteur][0]
                                else:
                                    self.c= self.c[:self.liste_calculs[compteur][0]-1-nombre_indice_a_retirer-int(compteur>0)] + [("x",compteur)] + self.c[self.liste_calculs[compteur][1] +1 -nombre_indice_a_retirer:]
                                    #print(f"nombre_indice_a_retirer = {nombre_indice_a_retirer} c sans les indices = {c}")
                                    nombre_indice_a_retirer+= self.liste_calculs[compteur][1]-self.liste_calculs[compteur][0]+1
                                compteur+= 1 
                                if compteur==len(self.liste_calculs):
                                    #print(f"liste_calculs = {liste_calculs} et resultat_final= {resultat_final} i={i} c={c} compteur={compteur}")
                                    break  
                                
                                
                        co= [list(self.c) for _ in range(2**self.colonnes)]#calcul final de l'expression
                        for i in range(len(co)):#calcul avec les valeurs des parenthèses
                            print(f"co = {co}     resultat_final = {resultat_final}")
                            for y in range(len(co[i])):
                                if co[i][y][0] == "x":
                                    co[i][y]= resultat_final[co[i][y][1]][i]
                            valeur= self.calcul([list(co[i]) for _ in range(2**self.colonnes)])[i]
                            self.grid.controls+= (self.texte(valeur),)


                def result(self):   
                    """
                    ajoute l'interface au tableau des vues
                    """
                    page.views.append(View("/calculatrice2",[
                        Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/calculatrice")),padding=padding.only(left=10,top=10)),
                        Container(self.grid
                        ,margin= margin.only(left=250),width=300,height=400)
                    ]))
                    self.calcul_final()

            Resultat().result()
        page.update()



    def view_pop(view):
        page.views.pop()#supprime la dernière vue, la vue principale actuelle.
        top_view = page.views[-1]#dernier element-> la dernière vue ajoutee devient la vue principale.
        page.go(top_view.route)#changement de vue.



    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

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
R2: Nombre = Nombre(30,False)
#print(N1.stats(R2,100))
#print(R1 + R2)
#print(N2._longueur)

#               INTERFACE               #

flet.app(target=main,assets_dir="assets")