from flet import Page,Text,Row,Column,ElevatedButton,TextButton,TextField,AppBar,View, colors
from nombre import *

def main(page : Page):
    page.theme_mode = "light"
    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Flet app"), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton("Visit Store", on_click=lambda _: page.go("/application1")),
                    
                    
                ],
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
        page.update()

    def view_pop(view):
        page.views.pop()#supprime la dernière vue, la vue principale actuelle.
        top_view = page.views[-1]#dernier element-> la dernière vue ajoutee devient la vue principale.
        page.go(top_view.route)#changement de vue.

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)