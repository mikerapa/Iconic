from textual.widget import Widget
from textual import on
from model.desktop_entry import DesktopEntry
from textual.app import ComposeResult
from textual.widgets import Label, Input
from ui.path_input import PathInput
from textual.validation import Function, ValidationResult
from textual.theme import Theme
from ui.file_path_input import FilePathInput

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

    def validate_name(self, name: str) -> bool:
        # the name should not be empty, contain special characters, start with a . or a /, and should be less than 256 characters
        name = name.strip()
        if not name:
            return False
        if len(name) > 256:
            return False
        if name[0] in ['.', '/']:
            return False
        if any(not c.isalnum() and c not in [' ', '_', '-', '.', '/'] for c in name):
            return False
        return True



    def compose(self) -> ComposeResult:
        print("Inside DesktopEntryEdit.compose")
        yield Label("Name:", classes="grid-label")
        yield Input(value=self.desktop_entry.name,id="name", validators=[Function(self.validate_name, "Name is invalid")])
        yield Label("Exec:")
        yield FilePathInput(id="exec", allow_files=True, allow_folders=False)
        yield Label("Icon:")
        yield FilePathInput(id="icon", allow_files=True, allow_folders=False)
        yield Label("Type:")
        yield Input(value=self.desktop_entry.type, id="type")
        yield Label("Categories:")
        yield Input(value=self.desktop_entry.categories, id="categories")

    @on(FilePathInput.PathSelected)
    def on_path_selected(self, event: FilePathInput.PathSelected):
        print(f"Path selected: {event.path}, id: {event.id}")

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed):
        print(f"Input changed {event.input.id}: {event.value}, valid: {event.validation_result}")
        if event.input.id == "name":
            self.desktop_entry.name = event.value
        elif event.input.id == "exec":
            self.desktop_entry.exec = event.value
        elif event.input.id == "icon":
            self.desktop_entry.icon = event.value
        elif event.input.id == "type":
            self.desktop_entry.type = event.value
        elif event.input.id == "categories":
            self.desktop_entry.categories = event.value

        if event.validation_result and event.validation_result.is_valid:
            event.input.styles.background = Theme.surface
        else:
            event.input.styles.background = Theme.error

