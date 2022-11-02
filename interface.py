from flet import Page,Text,Row,Column,ElevatedButton,TextButton,TextField,AppBar,View,colors,alignment,margin,Container,padding,ButtonStyle,Image,IconButton,icons,UserControl
from nombre import *

def main(page : Page):
    page.window_width = 703
    page.window_height = 550
    page.theme_mode = "light"
    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    Column(
                        controls=[
                            Container(content=Row(
                                controls=[
                                    TextButton("introduction", on_click=lambda _: page.go("/application1")),
                                    TextButton("application", on_click=lambda _: page.go("/application1")),
                                ],
                                alignment = "end"
                            ),padding=padding.only(top=10,right=10)),
                            Container(content=Text(value="algorithmie booléenne et son application au sein des ordinateurs",size = 30,),margin=margin.only(top=110),padding=padding.only(left=5,right=100)),
                            Container(
                                content=TextButton(
                                    "calculatrice",
                                    style = ButtonStyle(
                                        bgcolor="#3283FD",
                                        color="#FFFFFF",
                                        padding=padding.symmetric(vertical=13,horizontal=40)),
                                    on_click=lambda _: page.go("/calculatrice")),
                                padding=padding.only(left=5)
                                ),
                            Container(content=Image(src="\img_menu.png"),margin=margin.only(left=250),width=430)
                        ]
                    )
                ],
                padding=padding.only(left=10),
            )
        )
        if page.route == "/application1":
            entree1 = TextField(hint_text="Nombre 1")
            entree2 = TextField(hint_text="Nombre 2")
            resultat_add = Text(value="")
            def test(e):
                nombre1 = Nombre(int(entree1.value),False)
                nombre2 = Nombre(int(entree2.value),False)
                resultat_add.value=f"résultat= {nombre1+nombre2}"
                page.update()
            
            page.views.append(
                View(
                    "/application1",
                    [
                        AppBar(title=Text("Store"), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton("Menu", on_click=lambda _: page.go("/")),
                        Column(controls=[Row(controls=[entree1,entree2]),TextButton(text="addition",on_click=test),resultat_add]),
                    ],
                )
            )
        if page.route == "/calculatrice":#vue sous la forme d'une classe
            class calculatrice(UserControl):
                def __init__(self):
                    self.resultat= Text(value="out= A+B",size=30)
                    self.calcul=""
                    self.switch_symbol= Text("mode")
                    self.ope = [""]
                    self.ouverte=0
                
                def action_boutons(self,e):
                    operations=["not","or","and","xnor","xor","nor","nand"]
                    if len(self.ope)==1: self.resultat.value ="out= "#permet d'enlever le A and B par défaut. Il y a déjà un élement dans self.ope donc on compare la longueur avec 1
                    for i in range(len(operations)):#le but ici est d'itérer parmi les boutons possibles et de changer l'affichage en conséquence
                        
                        if e.control.data == operations[i]:
                            if self.ope[-1] in operations[1:] or e.control.data==self.ope[-1]:#permet d'empécher que deux signes se suivent sans lettre intermédiaire
                                break
                            operations_calcul=[u"\u0305","+","·","⊙","⊕","",""]#0305 correspond au code Unicode de la barre horizontale sur un élément.
                            
                            
                            #les lignes suivantes décrivent le cas où le not doit être distribué sur l'ensemble de la parenthèse
                            if e.control.data == "not" and self.ope[-1] in ["(",")"]:
                                inter=""#l'assignation par index n'est pas possible pour les strings, il faut donc créer une variable intermédiaire pour contenir les nouveaux élements.
                                morgan = False
                                for i in range(5,len(self.resultat.value)):#le start à 5 permet d'éviter le "out= "
                                    #nous devons traiter le cas où l'expression correspond à une des loi de morgan, auquel cas nous pouvons simplifier l'expression
                                    #nous vérifions donc si l'une des lois de morgan est verifiée par disjonction des cas.
                                    if self.resultat.value[i]=="(" and self.resultat.value[i+1] in ["A","B","C"]:
                                        if self.resultat.value[i+2]=="n" and self.resultat.value[i+3]in["+","·"] and self.resultat.value[i+4] in ["A","B","C"]:
                                            if self.resultat.value[i+5]=="n" and self.resultat.value[i+6]==")":
                                                morgan=True
                                            elif self.resultat.value[i+5] ==")":
                                                morgan=True
                                        if self.resultat.value[i+2]in["+","·"] and self.resultat.value[i+3] in ["A","B","C"]:
                                            if self.resultat.value[i+4]=="n" and self.resultat.value [i+5]==")":
                                                morgan= True
                                            elif self.resultat.value [i+4]==")":
                                                morgan = True
                                    if self.resultat.value[i]=="(":
                                        print(morgan)
                                    if morgan:
                                        if self.resultat.value[i]==u"\u0305":
                                            pass
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
                                self.resultat.value = f"out= {inter}"
                            

                            #les lignes suivantes décrivent le cas où le bouton a un symbole différent de not pour data out que le not ne doit pas être distribué.
                            else:
                                if len(self.ope)==1: self.resultat.value ="out= A"#place automatiquement la lettre A
                                self.resultat.value=f"out= {self.resultat.value[5:]}{operations_calcul[i]}"#[5:]permet d'enlever le "out=" dans la valeur du texte affiché.
                            self.ope.append(e.control.data)
                            break


                        #les lignes suivantes décrivent le cas où le bouton a une parenthèse pour data
                        elif e.control.data in ["(",")"]:
                            if  (e.control.data == "("and self.ope[-1] in ["A","B","C","not",")"]) or (e.control.data == ")"and self.ope[-1] in operations[1:]+[")"]) or (self.ope[-1]=="not"and self.ope[-2]==")"):#empêche les erreurs d'inattention
                                break
                            if e.control.data == "(":
                                self.ouverte+= 1
                                self.resultat.value=f"out= {self.resultat.value[5:]}("
                            elif e.control.data ==")" and self.ouverte >0:
                                self.resultat.value=f"out= {self.resultat.value[5:]})"
                                self.ouverte-= 1
                            else:
                                self.resultat.value=f"out= ({self.resultat.value[5:]})"
                            self.ope.append(e.control.data)
                            break


                        #les lignes suivantes décrivent le cas où le bouton a une lettre pour data
                        elif e.control.data in ["A","B","C"]:
                            if self.ope[-1] in ["A","B","C","not",")"]:#permet d'empécher que deux lettres se suivent sans signe intermédiaire.
                                break
                            self.resultat.value = f"out= {self.resultat.value[5:]}{e.control.data}"
                            self.ope.append(e.control.data)
                            break

                    print("\n\n")
                    page.update()



                def gate(self,nom,etat,texte):
                    if etat:
                        return TextButton(
                            content=Container(content=Image(src=f"\calc\{nom}.png"),width=67,height=90,bgcolor="#10000000",border_radius=10,padding=padding.symmetric(horizontal=10),alignment=alignment.center,),
                            on_click=self.action_boutons,
                            style=ButtonStyle(padding=padding.only(),overlay_color="#00000000"),
                            data=nom)
                    if texte:
                        return TextButton(
                            content=Container(content=Text(value=nom,size=40),width=67,height=90,bgcolor="#10000000",border_radius=10,padding=padding.symmetric(horizontal=10),alignment=alignment.center,),
                            on_click=self.action_boutons,
                            style=ButtonStyle(padding=padding.only(),color="#DA000000",overlay_color="#00000000"),
                            data=nom)
                    return Text(value=f"{nom}2")
                def changer_mode(e):
                    e.control.selected = not e.control.selected
                    e.control.update()
                def calc(self):
                    tableau_boutons= [self.gate("not",True,False),self.gate("or",True,False),self.gate("and",True,False),self.gate("A",False,True),self.gate("B",False,True),self.gate("C",False,True),self.gate("xnor",True,False),self.gate("xor",True,False),self.gate("nor",True,False),self.gate("nand",True,False),self.gate("(",False,True),self.gate(")",False,True)]
                    return View("/calculatrice",
                        [
                            Column(controls=[
                            Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/")),padding=padding.only(left=10,top=10)),
                            Container(content=self.resultat,margin=margin.only(top=30,left=20,bottom=40,right=10)),
                            Container(height=1.5,width=700,bgcolor="#78000000"),
                            Row(controls=[
                                Container(content=self.switch_symbol,margin=margin.only(left=30)),
                                IconButton(icon=icons.BATTERY_1_BAR,selected_icon=icons.BATTERY_FULL,selected=False,on_click=self.changer_mode,tooltip="changer le mode de représentation"),
                                Container(TextButton("calculer",
                                    style = ButtonStyle(
                                        bgcolor="#3283FD",
                                        color="#FFFFFF",
                                        padding=padding.symmetric(vertical=3,horizontal=20)),
                                    on_click=lambda _: page.go("/calculatrice")),margin=margin.only(left=450))
                                ],),
                            Container(height=1.5,width=700,bgcolor="#78000000"),
                            Container(content=Row(controls=tableau_boutons,wrap=True,spacing=37,run_spacing=14),padding=padding.symmetric(horizontal=50,vertical=20))
                    ])],padding=padding.only())
            page.views.append(calculatrice().calc())
        page.update()



    def view_pop(view):
        page.views.pop()#supprime la dernière vue, la vue principale actuelle.
        top_view = page.views[-1]#dernier element-> la dernière vue ajoutee devient la vue principale.
        page.go(top_view.route)#changement de vue.



    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)