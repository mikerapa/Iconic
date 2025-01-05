from textual.app import ComposeResult
from textual.widgets import Static
from ui.path_input import PathInput


class MainView(Static):
    """Main view container for the application"""

    def compose(self) -> ComposeResult:
        """Compose the main view layout"""
        yield PathInput()


