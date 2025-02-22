from textual.app import ComposeResult, on 
from textual import work 
from textual.containers import Vertical, Horizontal, HorizontalScroll, VerticalScroll
from textual.widget import Widget
from textual.widgets import Label, Static, Input, Button
from ui.file_path_input import FilePathInput
from ui.open_file import OpenFileModal
from ui.desktop_entry_edit import DesktopEntryEdit
from model.desktop_entry import DesktopEntry
from model.file_system import FileSystem
from textual.reactive import reactive
from ui.save_dialogs import SaveConfirmModal, SaveAsModal



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


# TODO: This file has some unused sytles



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
        yield FileSelectBar(self.selection_message)
        yield VerticalScroll( DesktopEntryEdit(self.desktop_file, classes="grid-scroll" ))
        yield Horizontal(Button("Save", id="save"), Button("Save As", id="save_as"), Button("Clear", id="clear"), classes="bottom-button-bar")
            
        

    def open_desktop_file(self, path: str):
        self.desktop_file = FileSystem.read_desktop_file(path)
        print(f"Desktop file opened: {self.desktop_file}")
        self.query_one(DesktopEntryEdit).desktop_entry = self.desktop_file

    



    @on(Button.Pressed, "#browse")
    def on_browse_button_pressed(self, event: Button.Pressed) -> None:
        def desktop_file_selected(path: str |None):
            if path:
                print(f"Desktop file selected: {path}")
                self.desktop_file_path = path
                self.selection_message = f"Editing {path}"
                self.query_one("#selection-message").update(self.selection_message)
                self.open_desktop_file(path)
            else:
                print("No desktop file selected")
            



        print("Button pressed")
        event.button.styles.animate("opacity", 0, duration=2.0)
        event.button.styles.animate("opacity", 1, duration=2.0)
        modal = OpenFileModal()
        returned_path = self.app.push_screen(modal, desktop_file_selected)


    @on(Button.Pressed, "#save")
    def on_save_button_pressed(self, event: Button.Pressed) -> None:
        print("on_save_button_pressed: ", self.desktop_file_path)
        if self.desktop_file_path:
            # Show confirmation dialog
            self.confirm_save()
        else:
            # Show save as dialog
            self.handle_save_as()

    @on(Button.Pressed, "#save_as")
    def on_save_as_button_pressed(self, event: Button.Pressed) -> None:
        self.handle_save_as()

    @work
    async def confirm_save(self) -> None:
        print("confirm_save: ", self.desktop_file_path)
        confirm_modal = SaveConfirmModal(self.desktop_file_path)
        if await self.app.push_screen_wait(confirm_modal):
            print("confirm_save: ", self.desktop_file_path, "desktop_file: ", self.desktop_file)
            FileSystem.write_desktop_file(self.desktop_file_path, self.desktop_file)


    @work
    async def handle_save_as(self) -> None:
        print("Saving as...")
        save_as_modal = SaveAsModal()
        # Wait for the modal to complete and get the result
        result = await self.app.push_screen_wait(save_as_modal)
        print("handle_save_as result: ", result)
        if result:
            FileSystem.write_desktop_file(result, self.desktop_file)
            self.desktop_file_path = result
            self.selection_message = f"Editing {result}"
            self.query_one("#selection-message").update(self.selection_message)
        else:
            print("No save path selected")

