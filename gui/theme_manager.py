"""
Theme Manager for SDM4055A-SC multimeter controller.
Manages theme switching and persistence.
"""

from typing import Optional
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings
from qt_material import apply_stylesheet


class ThemeManager(QObject):
    """
    Manages application theme switching and persistence.
    """

    # Signal emitted when theme changes
    theme_changed = Signal(str)  # Emits "dark" or "light"

    def __init__(self, app: QApplication, parent: Optional[QObject] = None):
        """
        Initialize theme manager.

        Args:
            app: QApplication instance.
            parent: Parent QObject.
        """
        super().__init__(parent)
        self._app = app
        self._current_theme = "dark"  # Default theme
        self._settings = QSettings("SDM4055A-SC", "Controller")

        # Load saved theme preference
        self._load_theme_preference()

    def _load_theme_preference(self) -> None:
        """Load theme preference from QSettings."""
        saved_theme = self._settings.value("theme", "dark")
        if saved_theme in ["dark", "light"]:
            self._current_theme = saved_theme
        else:
            self._current_theme = "dark"
        print(f"Loaded theme preference: {self._current_theme}")

    def _save_theme_preference(self) -> None:
        """Save theme preference to QSettings."""
        self._settings.setValue("theme", self._current_theme)
        self._settings.sync()
        print(f"Saved theme preference: {self._current_theme}")

    def get_current_theme(self) -> str:
        """
        Get current theme.

        Returns:
            Current theme string ("dark" or "light").
        """
        return self._current_theme

    def set_theme(self, theme: str) -> None:
        """
        Set application theme.

        Args:
            theme: Theme string ("dark" or "light").
        """
        if theme not in ["dark", "light"]:
            print(f"Invalid theme: {theme}, using dark theme")
            theme = "dark"

        self._current_theme = theme

        # Apply qt-material theme
        if theme == "dark":
            apply_stylesheet(self._app, theme='dark_teal.xml')
        else:
            apply_stylesheet(self._app, theme='light_teal.xml')

        # Save preference
        self._save_theme_preference()

        # Emit signal
        self.theme_changed.emit(theme)

        print(f"Applied theme: {theme}")

    def toggle_theme(self) -> None:
        """Toggle between dark and light themes."""
        new_theme = "light" if self._current_theme == "dark" else "dark"
        self.set_theme(new_theme)

    def apply_initial_theme(self) -> None:
        """Apply the initial theme based on saved preference."""
        if self._current_theme == "dark":
            apply_stylesheet(self._app, theme='dark_teal.xml')
        else:
            apply_stylesheet(self._app, theme='light_teal.xml')
        print(f"Applied initial theme: {self._current_theme}")
