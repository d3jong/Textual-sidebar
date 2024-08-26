from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Header, Footer, Static, Label
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

class SettingsView(Vertical):
    def __init__(self, id: str) -> None:
        super().__init__(id=id)
        self._label = Label("Settings:")
        self._update_button = Button("Update Settings")
        self._change_label_button = Button("Change Label")
        
        # Add widgets to the view
        self.mount(self._label)
        self.mount(self._update_button)
        self.mount(self._change_label_button)

        # Bind events to buttons
        self._update_button.on_click(self.on_update_button_click)
        self._change_label_button.on_click(self.on_change_label_button)

    def on_update_button_click(self) -> None:
        self._label.update("Settings Updated!")

    def on_change_label_button_click(self) -> None:
        self._label.update("Updated Settings Label")

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
                self._main_container = Vertical(id="main_container")
                yield self._main_container

    def on_mount(self) -> None:
        # Initialize main view
        self._main_content = MainView(id="main_view")
        self._main_container.mount(self._main_content)
        # Set initial button pressed state
        first_button = self.query("#sidebar Button").first()
        if first_button:
            first_button.press()

        log("Hello, World")  # simple string
        log(locals())  # Log local variables
        log(children=self.children, pi=3.141592)  # key/values
        log(self.tree)  # Rich renderables

    def on_button_pressed(self, event: SidebarButton.Pressed) -> None:
        if event.button.view_name == "home":
            self._update_main_view(MainView(id="main_view"))
            self.query_one("#main_view", MainView).update_content("Welcome to the Home view!")
        elif event.button.view_name == "settings":
            self._update_main_view(SettingsView(id="settings_view"))
        elif event.button.view_name == "about":
            self._update_main_view(MainView(id="main_view"))
            self.query_one("#main_view", MainView).update_content("About this application.")

    def _update_main_view(self, new_view):
        # Clear existing content by removing all widgets
        # for widget in list(self._main_container.children):
        #     print(widget)
        self._main_container.remove_children(list(self._main_container.children))
        # Mount new view
        self._main_container.mount(new_view)

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
