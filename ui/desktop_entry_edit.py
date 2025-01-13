from textual.widget import Widget
from model.desktop_entry import DesktopEntry
from textual.app import ComposeResult
from textual.widgets import Label, Input
from ui.path_input import PathInput


class DesktopEntryEdit(Widget):

    DEFAULT_CSS = """
    DesktopEntryEdit {
        border: solid $secondary;
        layout: grid;
        grid-size: 2 5;
        grid-columns: 1fr 8fr;
        grid-rows: 4;
    }


    """

    def __init__(self, desktop_entry: DesktopEntry, classes: str = ""):
        super().__init__(classes=classes)
        self.desktop_entry = desktop_entry

    def compose(self) -> ComposeResult:
        print("Inside DesktopEntryEdit.compose")
        yield Label("Name:", classes="grid-label")
        yield Input(value=self.desktop_entry.name)
        yield Label("Exec:")
        yield PathInput(allow_files=True, allow_folders=False)
        yield Label("Icon:")
        yield PathInput(allow_files=True, allow_folders=False)
        yield Label("Type:")
        yield Input(value=self.desktop_entry.type)
        yield Label("Categories:")
        yield Input(value=self.desktop_entry.categories)
