import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow

def main():
    """Main entry point for the application"""
    # Create the application
    app = QApplication(sys.argv)
    
    # Set application name and organization for settings
    app.setApplicationName("AI Text & Audio Tool")
    app.setOrganizationName("AI Dev")
    
    # Use Fusion style for consistent cross-platform appearance
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()