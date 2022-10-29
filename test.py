import flet
from flet import IconButton, Page, Row, TextField, icons, Image

def main(page: Page):
    page.title = "Flet counter example"
    page.vertical_alignment = "center"
    page.theme_mode = "light"

    page.add(Image(src="https://images.unsplash.com/photo-1666811260863-560f6b6e0e29?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHw0fHx8ZW58MHx8fHw%3D&auto=format&fit=crop&w=1100&q=60"))
    page.update()
    

flet.app(target=main)