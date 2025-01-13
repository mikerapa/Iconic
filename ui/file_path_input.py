from textual.widgets import Static, Button, Input, DirectoryTree, Label
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widget import Widget
from pathlib import Path #TODO: can this be removed?
import model.log_handler as log_handler
from typing import Iterable


logger = log_handler.get_logger(__name__)


class FilteredDirectoryTree(DirectoryTree):
    def filter(self, path: Path) -> bool:
        return path.is_dir() or (not self.select_directory and Path(path).match(self.pattern))
    
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if Path(path).match(self.pattern)]
    
    
    def __init__(self, pattern: str = "*", path: str = ".", select_directory: bool = False):
        super().__init__(path=path)
        self.pattern = pattern
        self.path = path
        self.select_directory = select_directory
        logger.info(f"FilteredDirectoryTree initialized with pattern: {pattern} path: {path} select_directory: {select_directory}")

class FileSelectModal(ModalScreen):
    """Modal screen for file/directory selection."""


    logger = log_handler.get_logger(__name__)
    
    def __init__(self, path: str = ".", pattern: str = "*", select_directory: bool = False):
        super().__init__()
        self.path = path
        self.pattern = pattern
        self.select_directory = select_directory
        self.selected_path = None

    def compose(self) -> ComposeResult:
        title = "Select a directory" if self.select_directory else "Select a file"
        yield Static(title, id="title")
        yield FilteredDirectoryTree(
            path=self.path, 
            pattern=self.pattern,
            select_directory=self.select_directory
        )
        yield Button("Select", variant="primary", id="select")
        yield Button("Cancel", variant="default", id="cancel")

    
    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.selected_path = event.node.data.path

        self.logger.info(f"Directory tree file selected: {event.node.data.path} selected_path: {self.selected_path}")    


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.logger.info("Cancel button pressed")
            self.dismiss()
        elif event.button.id == "select":
            self.logger.info(f"Select button pressed selected_path: {self.selected_path}")
            tree = self.query_one(FilteredDirectoryTree)
            if self.selected_path:
                
                if self.select_directory or (not self.select_directory and Path(self.selected_path).match(self.pattern)):
                    self.dismiss(self.selected_path)

class FilePathInput(Widget):
    """Widget for selecting file or directory paths."""
    DEFAULT_CSS = """
    .inline-widget {
        width: 40;
    }
    """

    def __init__(self, pattern: str = "*", select_directory: bool = False):
        self.pattern = pattern
        self.select_directory = select_directory
        self.path = ""
        super().__init__()



    def compose(self) -> ComposeResult:
        my_label = Label("testing")
        my_label.styles.width = "20"
        yield Horizontal(
            Input(value=self.path, classes="inline-widget"),
            my_label,
            Button("Browse", classes="inline-widget")
        )


    async def on_button_pressed(self, event: Button.Pressed) -> None:
        modal = FileSelectModal(".", self.pattern, self.select_directory)
        path = await self.app.push_screen(modal)
        if path:
            self.path = str(path)
            input_widget = self.query_one(Input)
            input_widget.value = self.path 