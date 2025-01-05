from textual.app import App
from ui.main_view import MainView
from model.log_handler import get_logger

logger = get_logger(__name__)

class IconicApp(App):
    """Main Iconic application."""
    
    def compose(self):
        """Create child widgets for the app."""
        yield MainView()

def main():
    logger.debug("Iconic started")
    app = IconicApp()
    app.run()

if __name__ == "__main__":
    # TODO: add command argument for log level
    main()
