from textual.app import ComposeResult, on
from textual.containers import Vertical, Horizontal, HorizontalScroll, VerticalScroll
from textual.widget import Widget
from textual.widgets import Label, Static, Input, Button
from ui.file_path_input import FilePathInput
from ui.desktop_entry_edit import DesktopEntryEdit
from model.desktop_entry import DesktopEntry
from model.file_system import FileSystem
from ui.open_file import OpenFileModal
from textual.reactive import reactive


class InputWithLabel(Widget):
    """An input with a label."""

    DEFAULT_CSS = """
    InputWithLabel {
        layout: horizontal;
        height: auto;
    }
    InputWithLabel Label {
        padding: 1;
        width: 12;
        text-align: right;
    }
    InputWithLabel Input {
        width: 1fr;
    }
    """

    def __init__(self, input_label: str) -> None:
        self.input_label = input_label
        super().__init__()

    def compose(self) -> ComposeResult:  
        yield Label(self.input_label)
        yield Input()

class FilePathInput2(Widget):
    """Widget for selecting file or directory paths."""

    # def __init__(self, pattern: str = "*", select_directory: bool = False):
    #     super().__init__()
    #     self.pattern = pattern
    #     self.select_directory = select_directory
    #     self.path = ""

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static("File Path Input", id="file-path-input-title")


class FileSelectBar(Widget):
    """Widget for selecting a file or directory path."""

    DEFAULT_CSS = """
    FileSelectBar {
        border: solid #444444;
        layout: horizontal;
        max-height: 5;
        background: #222222;
    }
    """

    def __init__(self, selection_message: str):
        super().__init__()
        self.selection_message = selection_message

    def compose(self) -> ComposeResult:
        yield Label(self.selection_message, id="selection-message", classes="attention_label inline")
        yield Button("Browse", id="browse")




class MainView(Widget):
    """Main view container for the application"""

    DEFAULT_CSS = """


    .attention_label{
        width: 2fr;
        # border: solid green;
        height: 3;
    }

    .inline{
        width: 1fr;
        padding: 1;
    }

    .dockTop{
        dock: top;
    }

    MainView {
        # border: solid blue;
    }

    """



    selection_message = reactive("Open a .desktop file to edit")

    def __init__(self):
        super().__init__()
        self.desktop_file_path = None
        self.desktop_file= DesktopEntry()
        # self.selection_message = "Open a .desktop file to edit"

    def compose(self) -> ComposeResult:
        """Compose the main view layout"""
        # selection_label = Label(self.selection_message, id="selection-message")
        # selection_label.styles.border = "solid green"
        yield FileSelectBar(self.selection_message)
        # yield Horizontal(Label(self.selection_message, id="selection-message", classes="attention_label inline"), Button("Browse", id="browse"))
        # yield DesktopEntryEdit(self.desktop_file )
        yield VerticalScroll( DesktopEntryEdit(self.desktop_file, classes="grid-scroll" ))
        yield Horizontal(Button("Save", id="save"), Button("Save As", id="save_as"), Button("Clear", id="clear"), classes="bottom-button-bar")
            
        
        # yield DesktopEntryEdit(self.desktop_file)


    def open_desktop_file(self, path: str):
        self.desktop_file = FileSystem.get_desktop_entry(path)


    @on(Button.Pressed, "#browse")
    def on_browse_button_pressed(self, event: Button.Pressed) -> None:
        def desktop_file_selected(path: str |None):
            if path:
                print(f"Desktop file selected: {path}")
                self.desktop_file_path = path
                self.selection_message = f"Editing {path}"
                self.query_one("#selection-message").update(self.selection_message)
            else:
                print("No desktop file selected")
            



        print("Button pressed")
        event.button.styles.animate("opacity", 0, duration=2.0)
        event.button.styles.animate("opacity", 1, duration=2.0)
        modal = OpenFileModal()
        returned_path = self.app.push_screen(modal, desktop_file_selected)
        # event.button.styles.animate("opacity", 1, duration=0.1)

            # yield FilePathInput(pattern="*.txt")
            # yield DesktopEntryEdit(DesktopEntry(name="Test", exec="test", icon="test", type="Application", categories=["Utility"]))
            # yield DesktopEntryEdit(DesktopEntry(name="Test", exec="test", icon="test", type="Application", categories=["Utility"]))

    
        # yield FilePathInput(pattern="*.desktop")
        # yield FilePathInput2()
        # yield Label("Desktop Entry Editor") 
            # yield FilePathInput(pattern="*.txt")

            # yield DesktopEntryEdit(DesktopEntry(name="Test", exec="test", icon="test", type="Application", categories=["Utility"]))
            # yield DesktopEntryEdit(DesktopEntry(name="Test", exec="test", icon="test", type="Application", categories=["Utility"]))

