from textual.app import ComposeResult
from textual.widget import Widget
from ui.path_input import PathInput
from ui.desktop_entry_edit import DesktopEntryEdit  
from model.desktop_entry import DesktopEntry
class MainView(Widget):
    """Main view container for the application"""

    def compose(self) -> ComposeResult:
        """Compose the main view layout"""
        # yield PathInput()
        
        yield DesktopEntryEdit(DesktopEntry(name="Test", exec="test", icon="test", type="Application", categories=["Utility"]))

