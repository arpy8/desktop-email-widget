import json
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Widget Configuration")
        self.setFixedSize(400, 250)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("First Time Setup")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Please enter your Gmail credentials to continue:")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your-email@gmail.com")
        form_layout.addRow("Email:", self.email_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("App Password")
        form_layout.addRow("App Password:", self.password_input)
        
        # Gemini API Key input
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Google Gemini API Key")
        form_layout.addRow("Gemini API Key:", self.api_key_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save & Continue")
        save_btn.clicked.connect(self.save_config)
        save_btn.setDefault(True)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def center_window(self):
        screen = self.parent().screen() if self.parent() else None
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def save_config(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        api_key = self.api_key_input.text().strip()
        
        if not email or not password or not api_key:
            QMessageBox.warning(self, "Invalid Input", 
                              "Please fill in all fields.")
            return
        
        if "@" not in email:
            QMessageBox.warning(self, "Invalid Email", 
                              "Please enter a valid email address.")
            return
        
        config = {
            "USER_EMAIL": email,
            "USER_PASSWORD": password,
            "GEMINI_API_KEY": api_key
        }
        
        try:
            with open("user_config.json", "w") as f:
                json.dump(config, f, indent=4)
            
            QMessageBox.information(self, "Success", 
                                  "Configuration saved successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Failed to save configuration: {str(e)}")
