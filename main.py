import os
import sys
import json
import importlib
import config
importlib.reload(config)

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
                        QLabel,
                        QVBoxLayout,
                        QWidget,
                        QApplication,
                        QDesktopWidget,
                        QShortcut,
                        QMessageBox
                    )

from llm import enhance_email_data
from mailer import get_last_n_mails
from config_dialog import ConfigDialog
from config import COLOR_MAP, has_config
from utils import WindowsAPIBS, show_toast


class HoverCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.3); color: white; font-size: 14px; padding: 5px; border-radius: 5px;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    def update_content(self, content):
        self.label.setText(content)

class Log(QLabel, WindowsAPIBS):
    def __init__(self, email_data=None, shared_canvas=None):
        super().__init__()
        
        self.email_body = email_data.get("body", "No content available")
        color = COLOR_MAP[email_data.get('priority', 'white')] if 'zs' not in email_data.get('from', '') else COLOR_MAP['zs']
        self.canvas = shared_canvas
        self.setText(f"{email_data.get('date', 'Unknown Date')}: {email_data.get('subject', 'No Subject')}")
        self.setStyleSheet(f"color: {color};background-color: rgba(0, 0, 0, 0.3)   ")
        
    def enterEvent(self, event):
        if self.canvas:
            self.canvas.update_content(self.email_body)
            screen = QDesktopWidget().screenGeometry()
            canvas_width = self.canvas.width()
            canvas_height = self.canvas.height()
            x = (screen.width() - canvas_width) // 2
            y = (screen.height() - canvas_height) // 2
            self.canvas.move(x, y+100)
            self.canvas.show()
        
    def leaveEvent(self, event):
        if self.canvas:
            self.canvas.hide()

class MainWindow(QWidget, WindowsAPIBS):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("color: lime; font-size: 14px;")
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.shared_canvas = HoverCanvas()
        
        self.emails = []
        self.max_emails = 10
        
        self.load_emails()
        
        self.setLayout(self.layout)
        self.position_at_bottom()

        self.email_timer = QTimer(self)
        self.email_timer.timeout.connect(self.fetch_and_update_emails)
        self.email_timer.start(15 * 60 * 1000)

        self.visibility_timer = QTimer(self)
        self.visibility_timer.timeout.connect(self.check_desktop_visibility)
        self.visibility_timer.start(50)
        self.hide()

        self.refresh_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.refresh_shortcut.activated.connect(self.fetch_and_update_emails)

    def load_emails(self):
        try:
            with open("logs.json", "r", encoding="utf-8") as f:
                all_emails = json.load(f)
            
            self.emails = all_emails[:self.max_emails]
            self.clear_layout()
            
            for email in self.emails:
                log = Log(email_data=email, shared_canvas=self.shared_canvas)
                self.layout.addWidget(log)
        except FileNotFoundError:
            self.emails = []

            if not os.path.exists("logs.json"):
                email_data = get_last_n_mails(10)
                enhanced_data = enhance_email_data(email_data)

                with open("logs.json", "w", encoding="utf-8") as f:
                    f.write(enhanced_data)

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def new_mail_exists(self, email_data, existing_logs):
        if not existing_logs:
            return True
        
        if isinstance(email_data, str):
            parsed_email_data = json.loads(email_data)
        else:
            parsed_email_data = email_data
        print(f"new mail: {parsed_email_data[0]["subject"] != existing_logs[0]["subject"]}")
        
        is_new_mail = parsed_email_data[0]["subject"] != existing_logs[0]["subject"]
        print(f"New mail exists: {is_new_mail}")
        
        if is_new_mail:
            show_toast(message=f"New {parsed_email_data[0]['priority']} priority mail received.")
            
        return is_new_mail

    def fetch_and_update_emails(self):
        try:
            print("Fetching new emails...")
            email_data = get_last_n_mails(1)
            
            try:
                with open("logs.json", "r", encoding="utf-8") as f:
                    existing_logs = json.load(f)
            except FileNotFoundError:
                existing_logs = []
            
            if self.new_mail_exists(email_data, existing_logs):
                enhanced_data = enhance_email_data(email_data) 
                new_email = json.loads(enhanced_data)[0] if isinstance(enhanced_data, str) else enhanced_data[0]
                existing_logs.insert(0, new_email)
                
                existing_logs = existing_logs[:10]
            
            with open("logs.json", "w", encoding="utf-8") as f:
                json.dump(existing_logs, f, indent=4, ensure_ascii=False)
            
            self.load_emails()
            print("Emails updated successfully")

        except Exception as e:
            print(f"Error fetching emails: {e}")

    def position_at_bottom(self):
        screen = QDesktopWidget().screenGeometry()
        widget_height = self.sizeHint().height()
        self.move(0, screen.height() - widget_height)

def check_first_time_setup():
    """Check if this is the first time running the application"""
    if not has_config():
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        dialog = ConfigDialog()
        result = dialog.exec_()
        
        if result == QApplication.Accepted:
            return True
        else:
            QMessageBox.information(None, "Setup Cancelled", 
                                  "Application cannot run without configuration.")
            return False
    return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not check_first_time_setup():
        sys.exit(1)
    
    clock = MainWindow()
    sys.exit(app.exec_())