"""
SDM4055A-SC Multimeter Controller - Main Entry Point

A modern GUI application for monitoring the Siglent SDM4055A-SC
5½ digit digital multimeter via USB using VISA protocol.
"""

import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath
from PySide6.QtCore import Qt, QSize

from gui import MainWindow, ThemeManager
import version


def create_multimeter_icon(size: int = 64) -> QIcon:
    """
    Create a custom multimeter icon for the application.
    
    The icon features a digital multimeter with:
    - A rectangular body with rounded corners
    - A digital display screen showing measurement values
    - Two probe connectors (red and black)
    - A modern, professional design
    
    Args:
        size: Icon size in pixels (default: 64)
    
    Returns:
        QIcon: The created multimeter icon
    """
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Scale factors for drawing
    scale = size / 64.0
    
    # Draw multimeter body (dark gray rounded rectangle)
    body_rect = (4 * scale, 8 * scale, 56 * scale, 48 * scale)
    painter.setPen(QPen(QColor(60, 60, 60), 2))
    painter.setBrush(QBrush(QColor(45, 45, 45)))
    painter.drawRoundedRect(*body_rect, 6 * scale, 6 * scale)
    
    # Draw display screen (light blue/teal gradient effect)
    screen_rect = (10 * scale, 14 * scale, 44 * scale, 18 * scale)
    painter.setPen(QPen(QColor(30, 30, 30), 1))
    painter.setBrush(QBrush(QColor(20, 40, 50)))
    painter.drawRoundedRect(*screen_rect, 2 * scale, 2 * scale)
    
    # Draw measurement value on screen (digital numbers)
    painter.setPen(QColor(0, 255, 200))
    font = painter.font()
    font.setPixelSize(10 * scale)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(int(screen_rect[0] + 2 * scale), int(screen_rect[1] + 12 * scale), "5.000 V")
    
    # Draw unit label below value
    font.setPixelSize(5 * scale)
    painter.setFont(font)
    painter.setPen(QColor(0, 200, 150))
    painter.drawText(int(screen_rect[0] + 30 * scale), int(screen_rect[1] + 15 * scale), "DC")
    
    # Draw red probe connector (top right)
    painter.setPen(QPen(QColor(40, 40, 40), 1))
    painter.setBrush(QBrush(QColor(200, 30, 30)))
    painter.drawEllipse(int(44 * scale), int(36 * scale), int(8 * scale), int(8 * scale))
    # Red probe inner circle
    painter.setBrush(QBrush(QColor(150, 20, 20)))
    painter.drawEllipse(int(46 * scale), int(38 * scale), int(4 * scale), int(4 * scale))
    
    # Draw black probe connector (bottom right)
    painter.setPen(QPen(QColor(40, 40, 40), 1))
    painter.setBrush(QBrush(QColor(40, 40, 40)))
    painter.drawEllipse(int(44 * scale), int(46 * scale), int(8 * scale), int(8 * scale))
    # Black probe inner circle
    painter.setBrush(QBrush(QColor(20, 20, 20)))
    painter.drawEllipse(int(46 * scale), int(48 * scale), int(4 * scale), int(4 * scale))
    
    # Draw brand label at bottom
    font.setPixelSize(4 * scale)
    painter.setFont(font)
    painter.setPen(QColor(120, 120, 120))
    painter.drawText(int(10 * scale), int(52 * scale), "SDM4055A")
    
    # Draw measurement mode indicator
    painter.setPen(QPen(QColor(0, 255, 200, 100), 1))
    painter.setBrush(Qt.NoBrush)
    painter.drawRect(int(12 * scale), int(38 * scale), int(26 * scale), int(14 * scale))
    
    # Draw mode symbols (V, A, Ω)
    font.setPixelSize(6 * scale)
    font.setBold(True)
    painter.setFont(font)
    painter.setPen(QColor(0, 200, 150))
    painter.drawText(int(14 * scale), int(48 * scale), "V")
    painter.setPen(QColor(100, 100, 100))
    painter.drawText(int(22 * scale), int(48 * scale), "A")
    painter.setPen(QColor(100, 100, 100))
    painter.drawText(int(30 * scale), int(48 * scale), "Ω")
    
    painter.end()
    
    return QIcon(pixmap)


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
    
    # Set application icon
    app_icon = create_multimeter_icon()
    app.setWindowIcon(app_icon)
    logger.info(f"Application icon set:isNull={app_icon.isNull()}, availableSizes={app_icon.availableSizes()}")
    
    # Additional Windows-specific fix for taskbar icon
    logger.info(f"Application name: {app.applicationName()}")
    logger.info(f"Window icon set on QApplication")

    # Initialize theme manager and apply saved theme
    theme_manager = ThemeManager(app)
    theme_manager.apply_initial_theme()
    logger.info(f"Applied initial theme: {theme_manager.get_current_theme()}")

    # Create and show main window
    window = MainWindow(version=version.__version__, theme_manager=theme_manager)
    window.show()
    logger.info("Main window displayed")

    # Run application event loop
    exit_code = app.exec()

    logger.info(f"Application exited with code {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
