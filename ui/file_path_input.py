from textual.widgets import Static, Button, Input, DirectoryTree, Label
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widget import Widget
from pathlib import Path #TODO: can this be removed?
import model.log_handler as log_handler
from typing import Iterable
from textual import work
from textual.message import Message
from textual.reactive import reactive

logger = log_handler.get_logger(__name__)


class FilteredDirectoryTree(DirectoryTree):
    def filter(self, path: Path) -> bool:
        if self.allow_folder and not self.allow_file:
            return path.is_dir()
        return path.is_dir() or (self.allow_file and Path(path).match(self.pattern))
    
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        if self.allow_folder and not self.allow_file:
            return [path for path in paths if path.is_dir()]
        return [path for path in paths if Path(path).match(self.pattern)]
    
    
    def __init__(self, pattern: str = "*", path: str = ".", allow_folder: bool = False, allow_file: bool = True):
        super().__init__(path=path)
        self.pattern = pattern
        self.path = path
        self.allow_folder = allow_folder
        self.allow_file = allow_file
        logger.info(f"FilteredDirectoryTree initialized with pattern: {pattern} path: {path} allow_folder: {allow_folder} allow_file: {allow_file}")

class FileSelectModal(ModalScreen[str | None]):
    """Modal screen for file/directory selection."""


    logger = log_handler.get_logger(__name__)
    
    def __init__(self, path: str = ".", pattern: str = "*", allow_folder: bool = False, allow_file: bool = True):
        super().__init__()
        self.path = path
        self.pattern = pattern
        self.allow_folder = allow_folder
        self.allow_file = allow_file
        self.selected_path = None

    def compose(self) -> ComposeResult:
        title = "Select a directory" if self.allow_folder else "Select a file"
        yield Static(title, id="title")
        yield FilteredDirectoryTree(
            path=self.path, 
            pattern=self.pattern,
            allow_folder=self.allow_folder,
            allow_file=self.allow_file
        )
        yield Horizontal(
            Button("Select", variant="primary", id="select"),
            Button("Cancel", variant="default", id="cancel")
        )

    
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
                
                if self.allow_folder or (not self.allow_folder and Path(self.selected_path).match(self.pattern)):
                    self.dismiss(self.selected_path)

class FilePathInput(Widget):
    """Widget for selecting file or directory paths."""
    DEFAULT_CSS = """
    .inline-widget {
    }

    FilePathInput {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 4fr 1fr;
    }
    """
    path = reactive("")

    def __init__(self, id: str, pattern: str = "*", allow_files: bool = False, allow_folders : bool = False):
        self.pattern = pattern
        self.allow_files = allow_files
        self.allow_folders = allow_folders
        super().__init__(id=id)


    class PathSelected(Message):
        def __init__(self, path: str, id: str):
            self.path = path
            self.id = id
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Input(classes="inline-widget", id=f"{self.id}_input")
        yield Button("Browse", classes="inline-widget", id=f"{self.id}_browse")

    def watch_path(self, path: str):
        print(f"Path changed: {path}")
        input_widget = self.query_one(f"#{self.id}_input", Input)
        input_widget.value = self.path 


    @work
    async def handle_browse_button_pressed(self, event: Button.Pressed) -> None:
        print("on_browse_button_pressed")
        modal = FileSelectModal(".", self.pattern, self.allow_folders)
        path = await self.app.push_screen_wait(modal)
        if path:
            self.path = str(path)
            input_widget = self.query_one(f"#{self.id}_input", Input)
            input_widget.value = self.path 
            self.post_message(self.PathSelected(self.path, self.id))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        modal = FileSelectModal(".", self.pattern, self.allow_folders)
        self.handle_browse_button_pressed(event)