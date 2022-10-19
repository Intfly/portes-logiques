import flet
from flet import Page,Text,Row,Column,ElevatedButton,TextButton,TextField

def main(page : Page):
    t = Text(value="Hello, world!", color="green")
    def test(e):
        t.value="oui"
        page.update()
    page.controls.append(Row(controls=[t,TextButton(text="non",on_click=test)]))
    page.update()

    

flet.app(target=main)