from textual.screen import ModalScreen
from textual.widgets import Button, Static, Input
from textual.containers import Horizontal
from textual.app import ComposeResult
from pathlib import Path

class SaveConfirmModal(ModalScreen[bool]):
    """Modal dialog for confirming file save."""

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def compose(self) -> ComposeResult:
        yield Static(f"Save changes to {self.file_path}?", id="question")
        with Horizontal():
            yield Button("Save", variant="primary", id="save")
            yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.dismiss(True)
        else:
            self.dismiss(False)

class SaveAsModal(ModalScreen[str | None]):
    """Modal dialog for saving file with a new name."""

    def __init__(self, initial_path: str = "."):
        super().__init__()
        self.initial_path = initial_path

    def compose(self) -> ComposeResult:
        yield Static("Save As", id="title")
        yield Input(placeholder="Enter file name", id="filename")
        with Horizontal():
            yield Button("Save", variant="primary", id="save")
            yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            filename = self.query_one("#filename").value
            if filename:
                if not filename.endswith(".desktop"):
                    filename += ".desktop"
                save_path = Path(self.initial_path) / filename
                self.dismiss(str(save_path))
        else:
            self.dismiss(None) 