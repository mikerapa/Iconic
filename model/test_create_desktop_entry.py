from model.desktop_entry import DesktopEntry
from model.desktop_entry_builder import DesktopEntryBuilder


def test_create_desktop_entry():
    # Arrange
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
    result = DesktopEntryBuilder.create_desktop_entry(entry)

    # Assert
    assert result == expected
