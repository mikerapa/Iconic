from textual.app import App
from ui.main_view import MainView
from model.log_handler import get_logger
from textual.widgets import Footer
from textual.binding import Binding
from textual import on
from ui.open_file import OpenFileModal

logger = get_logger(__name__)

class IconicApp(App):
    """Main Iconic application."""
    
    # TODO: this CSS claass should  be renamed to something more general

    CSS_PATH = "ui/file_input_style.tcss"
    BINDINGS = [
        Binding(key="^q", action="quit", description="Quit"),
        # Binding(key="d", action="toggle_dark", description="Toggle dark mode"),
        Binding(key="^n", action="new_entry", description="New Desktop Entry"),
        Binding(key="^o", action="open_entry", description="Open Desktop Entry"),
    ]


    def compose(self):
        """Create child widgets for the app."""
        yield MainView()
        # yield OpenFileModal()
        yield Footer()

    def action_new_entry(self) -> None:
        """Create a new desktop entry."""
        print("New desktop entry")

    def action_open_entry(self) -> None:
        """Open a desktop entry."""
        print("Open desktop entry")


def main():
    logger.debug("Iconic started")
    app = IconicApp()
    app.run()

if __name__ == "__main__":
    # TODO: add command argument for log level
    main()
