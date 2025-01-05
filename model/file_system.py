import os
from model.desktop_entry import DesktopEntry
from model.desktop_entry_builder import DesktopEntryBuilder
from model.log_handler import get_logger

class FileSystem:
    # Class-level logger
    logger = get_logger(__name__)

    @staticmethod
    def read_desktop_file(file_path: str) -> DesktopEntry:
        """Reads a .desktop file and returns a DesktopEntry object
        
        Args:
            file_path: Path to the .desktop file to read
            
        Returns:
            DesktopEntry object containing the parsed file contents
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            ValueError: If the file is not a valid .desktop file
        """
        FileSystem.logger.debug(f"Reading desktop file: {file_path}")
        
        if not os.path.exists(file_path):
            FileSystem.logger.error(f"Desktop file not found: {file_path}")
            raise FileNotFoundError(f"Desktop file not found: {file_path}")
            
        desktop_data = {}
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        if not lines or not lines[0].strip() == "[Desktop Entry]":
            FileSystem.logger.error(f"Invalid desktop entry file format: {file_path}")
            raise ValueError("Invalid desktop entry file format")
            
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                if key == "Categories":
                    # Remove trailing semicolon and split into list
                    categories = value.rstrip(';').split(';')
                    desktop_data[key.lower()] = categories
                else:
                    desktop_data[key.lower()] = value
                    
        entry = DesktopEntry(
            name=desktop_data.get('name', ''),
            exec=desktop_data.get('exec', ''),
            icon=desktop_data.get('icon', ''),
            type=desktop_data.get('type', ''),
            categories=desktop_data.get('categories', [])
        )
        
        FileSystem.logger.debug(f"Successfully read desktop file: {file_path}")
        return entry

    @staticmethod
    def write_desktop_file(file_path: str, desktop_entry: DesktopEntry) -> None:
        """Writes a DesktopEntry object to a .desktop file
        
        Args:
            file_path: Path to the .desktop file to write
            desktop_entry: DesktopEntry object containing the entry details
        """
        FileSystem.logger.debug(f"Writing desktop file: {file_path}")
        
        with open(file_path, 'w') as f:
            f.write(DesktopEntryBuilder.create_desktop_entry(desktop_entry))
            
        FileSystem.logger.debug(f"Successfully wrote desktop file: {file_path}")
