from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QGroupBox, QFormLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import pyqtSignal
from dotenv import load_dotenv, set_key, find_dotenv
from pathlib import Path
import os
from script import _is_valid_token

class LoginPage(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Overall Layout
        main_layout = QVBoxLayout()

        # Group API Token Entry
        group_box = QGroupBox("API Token")
        group_layout = QFormLayout()
        self.line_edit = QLineEdit()
        group_layout.addRow(QLabel("Enter your API Token:"), self.line_edit)
        group_box.setLayout(group_layout)

        # Buttons
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setIcon(QIcon("C:\\Users\\30243\\Pictures\\sw (2).jpg"))

        self.mem_button = QPushButton("Read From Memory")
        self.mem_button.clicked.connect(self.read_env)

        # Add elements to main layout
        main_layout.addWidget(group_box)
        main_layout.addWidget(self.submit_button)
        main_layout.addWidget(self.mem_button)

        # Set the layout
        self.setLayout(main_layout)

        # Custom Font
        font = QFont("Arial", 12)
        self.setFont(font)

    def read_env(self):
        load_dotenv(find_dotenv())
        self.line_edit.setText(os.environ.get('CANVAS_API_TOKEN', ''))

    def on_submit(self):
        api_token = self.line_edit.text()
        if _is_valid_token(api_token):
            self.write_env(api_token)
            self.login_successful.emit()
        else:
            self.show_error_message("Invalid or expired token. Please try again.")

    def write_env(self, api_token):
        env_path = find_dotenv()
        if not env_path:
            env_path = 'canvas notifyer/.env'
        set_key(env_path, 'CANVAS_API_TOKEN', api_token)
        load_dotenv(env_path)

    def show_error_message(self, message):
        msg = QMessageBox.critical(self, "Error", message)
