from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Label, Static
from textual.reactive import reactive
from textual import events
import os
import model.log_handler as log_handler


class FolderPathInput(Static):
    """A component for entering and validating a folder path"""

    logger = log_handler.get_logger(__name__)
    folder_path = reactive("")
    is_valid = reactive(False)
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Folder Path:", id="path_label")
            yield Input(placeholder="Enter folder path...", id="path_input")
            yield Label("Message", id="message_label")
    
    def on_mount(self) -> None:
        self.input = self.query_one("#path_input", Input)
        self.label = self.query_one("#path_label", Label)
        self.message_label = self.query_one("#message_label", Label)

        
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle changes to the input field"""
        self.logger.info(f"Input changed: {event.value}")
        self.folder_path = event.value  
        self.logger.info(f"Path: {self.folder_path}")
        self.validate_path()
        
    def validate_path(self, _: str | None = None) -> None:
        """Validate the current path and update styling"""
        self.is_valid = os.path.isdir(self.folder_path) if self.folder_path else False
        self.logger.info(f"Path is valid: {self.is_valid} {self.folder_path}")
        # Update styles based on validity
        invalid_style = "color: red"
        valid_style = "color: white"
        
        self.input.styles.color = "red" if not self.is_valid else "white"
        self.label.styles.color = "red" if not self.is_valid else "white"
        self.message_label.update(f"{self.folder_path} valid={self.is_valid}")
        
    def watch_folder_path(self, new_path: str | None = None) -> None:
        """Handle changes to the path"""
        self.logger.info(f"Path changed: {self.folder_path}")

class MainView(Static):
    """Main view container for the application"""

    def compose(self) -> ComposeResult:
        """Compose the main view layout"""
        yield FolderPathInput()


