from textual.widget import Widget
from model.desktop_entry import DesktopEntry
from textual.app import ComposeResult
from textual.widgets import Label, Input
from ui.path_input import PathInput


class DesktopEntryEdit(Widget):


    def __init__(self, desktop_entry: DesktopEntry):
        super().__init__()
        self.desktop_entry = desktop_entry

    def compose(self) -> ComposeResult:
        yield Label("Desktop Entry Editor")
        yield Label("Name:")
        yield Input(value=self.desktop_entry.name)
        yield Label("Exec:")
        yield PathInput(allow_files=True, allow_folders=False)
        yield Label("Icon:")
        yield PathInput(allow_files=True, allow_folders=False)
        yield Label("Type:")
        # # yield Input(value=self.desktop_entry.type)
        # yield Label("Categories:")
        # # yield Input(value=self.desktop_entry.categories)
