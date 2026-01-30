"""
Generate application icon file for SDM4055A-SC Controller.
This script creates an .ico file from the multimeter icon design.
"""

from PySide6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QIcon
from PySide6.QtCore import Qt
import os
import sys

def create_multimeter_icon(size: int = 256) -> QPixmap:
    """
    Create a custom multimeter icon for the application.
    
    The icon features a digital multimeter with:
    - A rectangular body with rounded corners
    - A digital display screen showing measurement values
    - Two probe connectors (red and black)
    - A modern, professional design
    
    Args:
        size: Icon size in pixels (default: 256 for high quality)
    
    Returns:
        QPixmap: The created multimeter icon
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
    
    return pixmap


def main():
    """Generate icon files in multiple sizes for Windows .ico format."""
    from PySide6.QtGui import QImage
    
    print("Generating application icon...")
    
    # Create output directory if it doesn't exist
    output_dir = "assets/icons"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create icon in multiple sizes for best quality
    sizes = [16, 32, 48, 64, 128, 256]
    pixmaps = []
    
    for size in sizes:
        print(f"Creating {size}x{size} icon...")
        pixmap = create_multimeter_icon(size)
        pixmaps.append(pixmap)
    
    # Save as .ico file with multiple sizes
    icon_path = os.path.join(output_dir, "app_icon.ico")
    QIcon(pixmaps[0]).addFile(icon_path)
    
    # Also save individual PNG files for reference
    for i, size in enumerate(sizes):
        pixmap = pixmaps[i]
        png_path = os.path.join(output_dir, f"app_icon_{size}x{size}.png")
        pixmap.save(png_path, "PNG")
        print(f"Saved {png_path}")
    
    # Create the .ico file using QImage
    # Windows .ico files need special handling
    largest = pixmaps[-1]
    largest.save(icon_path, "ICO")
    print(f"Saved {icon_path}")
    
    print("\nIcon generation complete!")
    print(f"Main icon file: {icon_path}")
    print("PNG reference files also created for preview")
    
    return 0


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    
    # Create QApplication for Qt operations
    app = QApplication(sys.argv)
    
    sys.exit(main())
