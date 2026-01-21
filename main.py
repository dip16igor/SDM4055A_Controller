"""
SDM4055A-SC Multimeter Controller - Main Entry Point

A modern GUI application for monitoring the Siglent SDM4055A-SC
5½ digit digital multimeter via USB using VISA protocol.
"""

import sys
import logging
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from gui import MainWindow
import version


def setup_logging() -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting SDM4055A-SC Controller...")

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("SDM4055A-SC Controller")
    app.setOrganizationName("SDM4055A-SC")

    # Apply qt-material dark theme
    apply_stylesheet(app, theme='dark_teal.xml')
    logger.info("Applied dark_teal theme")

    # Create and show main window
    window = MainWindow(version=version.__version__)
    window.show()
    logger.info("Main window displayed")

    # Run application event loop
    exit_code = app.exec()

    logger.info(f"Application exited with code {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
