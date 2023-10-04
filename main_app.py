import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PyQt5.QtGui import QIcon
from login_page import LoginPage
from main_page import MainAppPage

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        self.stacked_widget = QStackedWidget()

        self.login_page = LoginPage()
    

        self.stacked_widget.addWidget(self.login_page)
     

        self.setCentralWidget(self.stacked_widget)

        self.login_page.login_successful.connect(self.on_login_successful)
        self.setCentralWidget(self.stacked_widget)

    def on_login_successful(self):
        
        self.mainpage = MainAppPage()
        self.stacked_widget.addWidget(self.mainpage)
  
        self.stacked_widget.setCurrentIndex(1)
     

if __name__ == '__main__':
    app = QApplication(sys.argv)
 
    app.setStyleSheet("""
    QWidget {
        background-color: #333333;
        color: #FFFFFF;
    }
    QPushButton {
        background-color: #555555;
        border: 1px solid #FFFFFF;
    }
    QPushButton:hover {
        background-color: #666666;
    }
    """)
    app.setStyle("Fusion")
 
    QApplication.setApplicationName("Canvas Notifyer")
    window = MyApp()
    window.setWindowIcon(QIcon("resources/logo.png"))
    window.resize(1280,720)
    window.show()
    sys.exit(app.exec_())

