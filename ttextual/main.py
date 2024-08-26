from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Header, Footer, Static
from textual.reactive import reactive
from textual import log

class SidebarButton(Button):
    def __init__(self, label: str, view_name: str) -> None:
        super().__init__(label)
        self.view_name = view_name

class MainView(Static):
    content = reactive("Welcome to the Home view!")

    def update_content(self, new_content: str) -> None:
        self.content = new_content

    def render(self) -> str:
        return self.content

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield SidebarButton("Home", "home")
                yield SidebarButton("Settings", "settings")
                yield SidebarButton("About", "about")
            with Vertical(id="main"):
                yield MainView(id="main_view")

    def on_mount(self) -> None:
        first_button = self.query("#sidebar Button").first()
        if first_button:
            first_button.press()

        log("Hello, World")  # simple string
        log(locals())  # Log local variables
        log(children=self.children, pi=3.141592)  # key/values
        log(self.tree)  # Rich renderables

    def on_button_pressed(self, event: SidebarButton.Pressed) -> None:
        main_view = self.query_one("#main_view", MainView)
        if event.button.view_name == "home":
            main_view.update_content("Welcome to the Home view!")
        elif event.button.view_name == "settings":
            main_view.update_content("This is the Settings view.")
        elif event.button.view_name == "about":
            main_view.update_content("About this application.")

    CSS = """
    Horizontal {
        height: 1fr;
    }

    #sidebar {
        width: auto;
        background: #333;
        color: white;
        padding: 1;
    }

    #main {
        padding: 1;
        height: 1fr;
    }

    Button {
        margin-bottom: 1;
        background: #444;
        border: none;
    }

    Button:focus {
        background: #555;
    }

    Button:hover {
        background: orange;
    }
    """

if __name__ == "__main__":
    app = MyApp()
    app.run()
