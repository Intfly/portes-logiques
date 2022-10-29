from tkinter.ttk import Style
from turtle import bgcolor, onclick
from flet import Page,Text,Row,Column,ElevatedButton,TextButton,TextField,AppBar,View,colors,alignment,margin,Container,padding,ButtonStyle,Image,IconButton,icons
from nombre import *

def main(page : Page):
    page.window_width = 700
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
            resultat = Text(value="")
            def test(e):
                nombre1 = Nombre(int(entree1.value),False)
                nombre2 = Nombre(int(entree2.value),False)
                resultat.value=f"résultat= {nombre1+nombre2}"
                page.update()
            
            page.views.append(
                View(
                    "/application1",
                    [
                        AppBar(title=Text("Store"), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton("Menu", on_click=lambda _: page.go("/")),
                        Column(controls=[Row(controls=[entree1,entree2]),TextButton(text="addition",on_click=test),resultat]),
                    ],
                )
            )
        if page.route == "/calculatrice":
            resultat= Text(value="out= A+B",size=30)
            def gate(nom,etat,texte):
                if etat:
                    return Container(content=Image(src=f"\calc\{nom}.png"),width=67,height=90,bgcolor="#10000000",border_radius=10,padding=padding.symmetric(horizontal=10),alignment=alignment.center,)
                if texte:
                    return Container(content=Text(value=nom,size=40),width=67,height=90,bgcolor="#10000000",border_radius=10,padding=padding.symmetric(horizontal=10),alignment=alignment.center,)
                return Text(value=f"{nom}2")

            switch_symbol= Text("mode")
            tableau_boutons= [gate("not",True,False),gate("or",True,False),gate("and",True,False),gate("A",False,True),gate("B",False,True),gate("C",False,True),gate("xnor",True,False),gate("xor",True,False),gate("nor",True,False),gate("nand",True,False),gate("(",False,True),gate(")",False,True)]
            def changer_mode(e):
                e.control.selected = not e.control.selected
                e.control.update()
            page.views.append(
                View("/calculatrice",
                [
                    Column(controls=[
                    Container(content=TextButton(content=Image(src="\_bouton_retour.png"),width=50,height=50,on_click=lambda _:page.go("/")),padding=padding.only(left=10,top=10)),
                    Container(content=resultat,margin=margin.only(top=30,left=20,bottom=40,right=10)),
                    Container(height=1.5,width=700,bgcolor="#78000000"),
                    Row(controls=[
                        Container(content=switch_symbol,margin=margin.only(left=30)),
                        IconButton(icon=icons.BATTERY_1_BAR,selected_icon=icons.BATTERY_FULL,selected=False,on_click=changer_mode,tooltip="changer le mode de représentation"),
                        Container(TextButton("calculer",
                            style = ButtonStyle(
                                bgcolor="#3283FD",
                                color="#FFFFFF",
                                padding=padding.symmetric(vertical=3,horizontal=20)),
                            on_click=lambda _: page.go("/calculatrice")),margin=margin.only(left=450))
                        ],),
                    Container(height=1.5,width=700,bgcolor="#78000000"),
                    Container(content=Row(controls=tableau_boutons,wrap=True,spacing=37,run_spacing=14),padding=padding.symmetric(horizontal=50,vertical=20))
            ])],padding=padding.only(),))
        page.update()

    def view_pop(view):
        page.views.pop()#supprime la dernière vue, la vue principale actuelle.
        top_view = page.views[-1]#dernier element-> la dernière vue ajoutee devient la vue principale.
        page.go(top_view.route)#changement de vue.

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)