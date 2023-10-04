from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox

from PyQt5.QtCore import pyqtSignal, QRect, QTimer
from dotenv import set_key,load_dotenv,find_dotenv
from pathlib import Path
from script import _is_valid_token
import os

class LoginPage(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        

        layout = QVBoxLayout()
 
        self.label = QLabel("Enter your API Token:")
        layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        #self.load_lbl = QLabel(self)
        #self.load_lbl.setGeometry(QRect(0, 0, 300, 300))

        #self.movie = QMovie("D:/project/canvas notifyer/resources/load.gif")
        #self.load_lbl.setMovie(self.movie)

        #layout.addWidget(self.load_lbl)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)

        self.mem_button = QPushButton("Read From Memory")
        self.mem_button.clicked.connect(self.read_env)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.mem_button)

        self.setLayout(layout)
    def read_env(self):
        load_dotenv(find_dotenv())
        api_token = os.environ.get('CANVAS_API_TOKEN')
        if api_token:
            obscured_token = api_token[0:11]+'*' * (len(api_token) - 11) 
            self.line_edit.setText(obscured_token)
        QTimer.singleShot(100, lambda: self.login(api_token))
    def login(self,api_token):
        if _is_valid_token(api_token):
            self.write_env(api_token)
            self.login_successful.emit()
        else:
            self.show_error_message("Invalid or expired token. Please try again.")

    def on_submit(self):
        api_token = self.line_edit.text()
        self.login(api_token)
    def show_error_message(self, message):
        msg = QMessageBox.critical(self, "Error", message)
        
   

    def write_env(self, api_token):
        env_path = find_dotenv()
        if not env_path:
            env_path = 'canvas notifyer/.env'
        set_key(env_path, 'CANVAS_API_TOKEN', api_token)
        load_dotenv(env_path)









