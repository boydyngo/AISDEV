import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton,
    QTextEdit, QMenuBar, QLabel, QStatusBar, QHBoxLayout
)
from PyQt6.QtGui import QPalette, QColor, QAction
from PyQt6.QtCore import Qt, pyqtSlot

from app.modules.tts_module import TTSModule
from app.services.ai_service import AIService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Text & Audio Tool")
        self.setGeometry(100, 100, 900, 700)

        # Initialize services
        self.ai_service = AIService()

        # --- Central Widget & Layout ---
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # --- Text Input Area ---
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter text here or load a document...")
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.main_layout.addWidget(self.text_edit)

        # --- Document Controls ---
        doc_controls = QHBoxLayout()
        self.new_doc_button = QPushButton("New Document")
        self.open_doc_button = QPushButton("Open Document")
        self.new_doc_button.clicked.connect(self.on_new_document)
        self.open_doc_button.clicked.connect(self.on_open_document)
        doc_controls.addWidget(self.new_doc_button)
        doc_controls.addWidget(self.open_doc_button)
        doc_controls.addStretch()
        self.main_layout.addLayout(doc_controls)

        # --- TTS Module ---
        self.tts_label = QLabel("Text-to-Speech")
        self.tts_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.main_layout.addWidget(self.tts_label)
        
        self.tts_module = TTSModule(self.ai_service)
        self.main_layout.addWidget(self.tts_module)

        # --- Placeholders for other modules ---
        self.stt_label = QLabel("Speech-to-Text")
        self.stt_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.main_layout.addWidget(self.stt_label)
        
        self.stt_placeholder = QLabel("Speech-to-Text module will be implemented here")
        self.main_layout.addWidget(self.stt_placeholder)

        self.transform_label = QLabel("Text Transformation")
        self.transform_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.main_layout.addWidget(self.transform_label)
        
        self.transform_placeholder = QLabel("Text Transformation module will be implemented here")
        self.main_layout.addWidget(self.transform_placeholder)

        # --- Status Bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # --- Menu Bar ---
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.setup_menus()

        # --- Theme ---
        self.is_dark_mode = False
        self._apply_theme()  # Apply initial theme

        # Set initial demo text and update TTS module
        self.set_demo_text()

    def setup_menus(self):
        # File Menu
        file_menu = self.menu_bar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.triggered.connect(self.on_new_document)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open...", self)
        open_action.triggered.connect(self.on_open_document)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.on_save_document)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = self.menu_bar.addMenu("Edit")
        
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        # View Menu
        view_menu = self.menu_bar.addMenu("View")
        
        theme_action = QAction("Toggle Dark Mode", self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)

        # Help Menu
        help_menu = self.menu_bar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    @pyqtSlot()
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self._apply_theme()

    def _apply_theme(self):
        palette = QPalette()
        if self.is_dark_mode:
            # Define Dark Mode Colors
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
            palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            # Set colors for disabled states
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(127, 127, 127))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(127, 127, 127))
            palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(127, 127, 127))
        else:
            # Reset to default system palette for light mode
            palette = QPalette()

        QApplication.instance().setPalette(palette)
        self.status_bar.showMessage(f"Switched to {'Dark' if self.is_dark_mode else 'Light'} Mode")

    def on_text_changed(self):
        # Update the text for TTS module whenever text changes
        current_text = self.text_edit.toPlainText()
        self.tts_module.set_text(current_text)

    def on_new_document(self):
        self.text_edit.clear()
        self.status_bar.showMessage("New document created")

    def on_open_document(self):
        # This is a placeholder - would implement file dialog and loading
        self.status_bar.showMessage("Document open dialog would appear here")

    def on_save_document(self):
        # This is a placeholder - would implement file dialog and saving
        self.status_bar.showMessage("Document save dialog would appear here")

    def show_about(self):
        # This is a placeholder - would implement an About dialog
        self.status_bar.showMessage("AI Text & Audio Tool - A versatile text and audio processing application")

    def set_demo_text(self):
        demo_text = "Welcome to the AI-Powered Text and Audio Tool. This application is designed to improve text and audio workflows for users who need accessibility features, content creators, and anyone who works extensively with text and audio."
        self.text_edit.setPlainText(demo_text)

    def closeEvent(self, event):
        # Clean up resources when closing the application
        self.tts_module.cleanup()
        event.accept()