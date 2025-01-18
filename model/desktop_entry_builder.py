from model.log_handler import get_logger

class DesktopEntryBuilder:
    # Class-level logger, initialized once when the class is defined
    logger = get_logger(__name__)

    @staticmethod
    def create_desktop_entry(desktop_entry) -> str:
        """Creates a .desktop entry file content from a DesktopEntry object
        
        Args:
            desktop_entry: DesktopEntry object containing the entry details
            
        Returns:
            String containing the .desktop file content in the correct format
        """
        DesktopEntryBuilder.logger.debug(f"Creating desktop entry for {desktop_entry.name}")
        
        content = "[Desktop Entry]\n"
        content += f"Name={desktop_entry.name}\n"
        content += f"Exec={desktop_entry.exec}\n"
        content += f"Icon={desktop_entry.icon}\n"
        content += f"Type={desktop_entry.type}\n"
        content += f"Categories={desktop_entry.categories}\n"
        
        DesktopEntryBuilder.logger.debug("Desktop entry created successfully")
        return content
