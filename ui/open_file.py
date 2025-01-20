from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Input, Label, Static
from textual.screen import Screen, ModalScreen
from ui.file_path_input import FilteredDirectoryTree
from textual import on


class OpenFileModal(ModalScreen[str | None]):
    """Modal screen for file/directory selection."""
    #TODO: This class may be redundant, as the FilePathInput widget can be used to select a file or directory
    #TODO: This file may be too specific to .desktop files

    
    def __init__(self, path: str = ".", pattern: str = "**.desktop", select_directory: bool = False):
        super().__init__()
        self.path = path
        self.pattern = pattern
        self.select_directory = select_directory
        self.selected_path = None

    def compose(self) -> ComposeResult:
        yield Static("Open File", id="title")
        yield FilteredDirectoryTree(
            path=self.path, 
            pattern=self.pattern,
            allow_folder=self.select_directory
        )
        yield Horizontal(Button("Select", variant="primary", id="select"), Button("Cancel", variant="default", id="cancel"))

    @on(FilteredDirectoryTree.FileSelected)
    def on_filtered_directory_tree_file_selected(self, event: FilteredDirectoryTree.FileSelected) -> None:
        print(f"File selected in tree event: {event.path}")
        self.selected_path = event.path


    @on(Button.Pressed, "#select")
    def on_select_button_pressed(self) -> None:
        self.dismiss(self.selected_path)

    @on(Button.Pressed, "#cancel")
    def on_cancel_button_pressed(self) -> None:
        self.dismiss()