
import os
import pytest
from model.desktop_entry import DesktopEntry
from model.file_system import FileSystem


def test_read_desktop_file():
    # Arrange
    test_file = "test_files/test.desktop"
    test_content = "[Desktop Entry]\n" + \
                   "Name=Test App\n" + \
                   "Exec=/usr/bin/test\n" + \
                   "Icon=/usr/share/icons/test.png\n" + \
                   "Type=Application\n" + \
                   "Categories=Development;Testing;\n"
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    expected = DesktopEntry(
        name="Test App",
        exec="/usr/bin/test",
        icon="/usr/share/icons/test.png",
        type="Application",
        categories=["Development", "Testing"]
    )
    
    # Act
    result = FileSystem.read_desktop_file(test_file)

    # Assert
    assert result == expected
    
    # Cleanup
    os.remove(test_file)


def test_read_desktop_file_not_found():
    # Arrange
    non_existent_file = "test_files/nonexistent.desktop"
    
    # Act & Assert
    with pytest.raises(FileNotFoundError):
        FileSystem.read_desktop_file(non_existent_file)


def test_read_desktop_file_invalid_format():
    # Arrange
    test_file = "test_files/invalid.desktop"
    with open(test_file, 'w') as f:
        f.write("Invalid content\n")
    
    # Act & Assert
    with pytest.raises(ValueError):
        FileSystem.read_desktop_file(test_file)
    
    # Cleanup
    os.remove(test_file)


def test_write_desktop_file():
    # Arrange
    test_file = "test_files/write_test.desktop"
    entry = DesktopEntry(
        name="Test App",
        exec="/usr/bin/test",
        icon="/usr/share/icons/test.png",
        type="Application",
        categories=["Development", "Testing"]
    )
    
    expected = "[Desktop Entry]\n" + \
               "Name=Test App\n" + \
               "Exec=/usr/bin/test\n" + \
               "Icon=/usr/share/icons/test.png\n" + \
               "Type=Application\n" + \
               "Categories=Development;Testing;\n"
    
    # Act
    FileSystem.write_desktop_file(test_file, entry)
    
    # Assert
    with open(test_file, 'r') as f:
        content = f.read()
    assert content == expected
    
    # Cleanup
    os.remove(test_file)


def test_check_path():
    """Test the check_path method with different combinations of allow_folders and allow_files"""
    # Create test folder and file
    test_folder = "test_folder"
    test_file = "test_file.txt"
    os.makedirs(test_folder, exist_ok=True)
    with open(test_file, 'w') as f:
        f.write("test")

    try:
        # Test with both folders and files allowed (default)
        assert FileSystem.check_path(test_folder) == True
        assert FileSystem.check_path(test_file) == True  # Default prioritizes folders

        # Test with only folders allowed
        assert FileSystem.check_path(test_folder, allow_folders=True, allow_files=False) == True
        assert FileSystem.check_path(test_file, allow_folders=True, allow_files=False) == False

        # Test with only files allowed
        assert FileSystem.check_path(test_folder, allow_folders=False, allow_files=True) == False
        assert FileSystem.check_path(test_file, allow_folders=False, allow_files=True) == True

        # Test with neither allowed
        assert FileSystem.check_path(test_folder, allow_folders=False, allow_files=False) == False
        assert FileSystem.check_path(test_file, allow_folders=False, allow_files=False) == False

        # Test with nonexistent path
        assert FileSystem.check_path("nonexistent", allow_folders=True, allow_files=True) == False

    finally:
        # Clean up test files
        os.remove(test_file)
        os.rmdir(test_folder)
