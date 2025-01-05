from textual.containers import Vertical
from textual.widgets import Input, Label, Static
from textual.reactive import reactive
from textual.app import ComposeResult
import os
from model.file_system import FileSystem
import model.log_handler as log_handler


class PathInput(Static):
    """A component for entering and validating a folder path"""

    logger = log_handler.get_logger(__name__)
    folder_path = reactive("")
    is_valid = reactive(False)
    
    def __init__(self, allow_folders: bool = True, allow_files: bool = True):
        super().__init__()
        self.allow_folders = allow_folders
        self.allow_files = allow_files



    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(
                "Folder Path:" if self.allow_folders and not self.allow_files else
                "File Path:" if not self.allow_folders and self.allow_files else
                "Path:",
                id="path_label"
            )
            yield Input(placeholder="Enter folder path...", id="path_input")
    
    def on_mount(self) -> None:
        self.input = self.query_one("#path_input", Input)
        self.label = self.query_one("#path_label", Label)

        
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle changes to the input field"""
        self.logger.info(f"Input changed: {event.value}")
        self.folder_path = event.value  
        self.logger.info(f"Path: {self.folder_path}")
        self.validate_path()
        
    def validate_path(self, _: str | None = None) -> None:
        """Validate the current path and update styling"""
        self.is_valid = FileSystem.check_path(self.folder_path, allow_folders=self.allow_folders, allow_files=self.allow_files)
        self.logger.info(f"Path is valid: {self.is_valid} {self.folder_path}")
        # Update styles based on validity
        invalid_style = "color: red"
        valid_style = "color: white"
        self.logger.info(f"Path is valid: {self.is_valid} {self.folder_path}")
        # Update styles based on validity
        invalid_style = "color: red"
        valid_style = "color: white"
        
        self.input.styles.color = "red" if not self.is_valid else "white"
        self.label.styles.color = "red" if not self.is_valid else "white"
        
    def watch_folder_path(self, new_path: str | None = None) -> None:
        """Handle changes to the path"""
        self.logger.info(f"Path changed: {self.folder_path}")