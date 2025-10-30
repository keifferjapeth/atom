#!/usr/bin/env python3
"""
Demo script to showcase the Siri-like glowing placeholder effect.
This is a minimal version that doesn't require all Atom dependencies.
"""
import sys
try:
    from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
    from PyQt6.QtGui import QPalette
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout,
        QLabel, QLineEdit, QPushButton, QTextEdit
    )
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("❌ PyQt6 not installed. Install with: pip install PyQt6")
    sys.exit(1)


class GlowingLineEdit(QLineEdit):
    """Custom QLineEdit with Siri-like glowing placeholder animation."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._glow_opacity = 0.3
        self._glow_animation = QPropertyAnimation(self, b"glowOpacity")
        self._glow_animation.setDuration(1500)
        self._glow_animation.setStartValue(0.3)
        self._glow_animation.setEndValue(0.9)
        self._glow_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._glow_animation.setLoopCount(-1)  # Loop forever
        
        # Start the animation
        self._glow_animation.start()
        
        # Apply initial styling
        self._update_style()
    
    @pyqtProperty(float)
    def glowOpacity(self):
        return self._glow_opacity
    
    @glowOpacity.setter
    def glowOpacity(self, value):
        self._glow_opacity = value
        self._update_style()
    
    def _update_style(self):
        """Update the stylesheet with current glow opacity."""
        # Calculate the glow color based on opacity
        glow_intensity = int(100 + (155 * self._glow_opacity))
        
        # Create a glowing effect similar to Siri
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid rgba({glow_intensity}, {glow_intensity}, {glow_intensity + 50}, {self._glow_opacity});
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: palette(base);
                selection-background-color: palette(highlight);
            }}
            QLineEdit:focus {{
                border: 2px solid rgba(100, 150, 255, {0.5 + self._glow_opacity * 0.5});
                box-shadow: 0 0 10px rgba(100, 150, 255, {self._glow_opacity});
            }}
        """)


class DemoWindow(QMainWindow):
    """Demo window to showcase the glowing effect."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atom AI - Siri-like Glowing Effect Demo")
        self.setMinimumSize(600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🌟 Siri-like Glowing Placeholder Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Watch the input field below pulse with a smooth, Siri-like glow effect.\n"
            "The border animates continuously, creating an elegant and modern interface."
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: gray; margin-bottom: 20px;")
        layout.addWidget(desc)
        
        # Glowing input field
        self.glowing_input = GlowingLineEdit()
        self.glowing_input.setPlaceholderText("Ask Atom to do something... ✨")
        self.glowing_input.setMinimumHeight(50)
        layout.addWidget(self.glowing_input)
        
        # Standard input for comparison
        comparison_label = QLabel("Standard Input (for comparison):")
        comparison_label.setStyleSheet("font-size: 12px; margin-top: 20px;")
        layout.addWidget(comparison_label)
        
        standard_input = QLineEdit()
        standard_input.setPlaceholderText("Regular placeholder without animation")
        standard_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid gray;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
        """)
        layout.addWidget(standard_input)
        
        # Info text
        info = QTextEdit()
        info.setReadOnly(True)
        info.setMaximumHeight(150)
        info.setPlainText(
            "✨ Features of the Glowing Effect:\n\n"
            "• Smooth pulsing animation (1.5 second cycle)\n"
            "• Color intensity changes from 30% to 90% opacity\n"
            "• Enhanced focus state with blue glow\n"
            "• Professional, modern appearance\n"
            "• Similar to Siri's visual feedback\n\n"
            "This effect provides subtle visual feedback that the system\n"
            "is ready and responsive, improving user experience."
        )
        info.setStyleSheet("font-family: 'SF Mono', monospace; font-size: 12px;")
        layout.addWidget(info)
        
        # Test button
        test_button = QPushButton("🎨 Test the Input")
        test_button.clicked.connect(self.test_input)
        test_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(test_button)
        
        central_widget.setLayout(layout)
    
    def test_input(self):
        """Test function for the button."""
        text = self.glowing_input.text()
        if text:
            self.glowing_input.clear()
            self.glowing_input.setPlaceholderText(f"You typed: {text} ✅")
        else:
            self.glowing_input.setPlaceholderText("Type something first! 💬")


def main():
    """Run the demo application."""
    if not PYQT_AVAILABLE:
        print("Cannot run demo without PyQt6")
        return 1
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show window
    window = DemoWindow()
    window.show()
    
    print("\n✨ Demo is running!")
    print("Watch the glowing placeholder animation in the input field.")
    print("Close the window to exit.\n")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
