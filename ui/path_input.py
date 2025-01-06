from textual.containers import Vertical
from textual.widgets import Input, Label, Static
from textual.reactive import reactive
from textual.app import ComposeResult
from textual import events
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

        
    def on_key(self, event: events.Key) -> None:
        self.logger.info(f"Key pressed: {event.key}")   
        """Handle key events in the input field"""
        if event.key == "tab":
            self.logger.info(f"Tab key pressed")
            current_path = self.input.value
            # Get the directory and partial name
            directory = os.path.dirname(current_path) if current_path else "."
            partial_name = os.path.basename(current_path)
            
            try:
                # List all matching items in the directory
                matches = [f for f in os.listdir(directory) 
                          if f.startswith(partial_name) and
                          (os.path.isfile(os.path.join(directory, f)) and self.allow_files or
                           os.path.isdir(os.path.join(directory, f)) and self.allow_folders)]
                
                if matches:
                    # Complete with the first match
                    completion = matches[0]
                    if directory == ".":
                        new_path = completion
                    else:
                        new_path = os.path.join(directory, completion)
                    
                    # Add trailing slash for directories
                    if os.path.isdir(new_path):
                        new_path = os.path.join(new_path, "")
                    
                    self.input.value = new_path
                    # Move cursor to end
                    self.input.cursor_position = len(new_path)
            except (OSError, PermissionError) as e:
                self.logger.error(f"Error during path completion: {e}")
            
            # Prevent default tab behavior
            event.prevent_default()


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