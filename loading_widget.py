from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QMovie, QFontDatabase, QFont
from PyQt5.QtCore import Qt, QSize
import os
class LoadingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set up loading animation
        self.loading_label = QLabel(self)
        self.loading_movie = QMovie("resources/load.gif")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, 'resources/Aurebesh/Aurebesh.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        _fontstr = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.custom_font = QFont(_fontstr)  # Use the first font family loaded
        self.custom_font.setPointSize(40) 

        self.loading_label.setMovie(self.loading_movie)
        self.loading_text = QLabel("LOADING")  # Text label for loading
        self.loading_text.setFont(self.custom_font)
        #self.loading_text.hide()  # Initially hidden
        

        
        self.loading_movie.setScaledSize(QSize(200, 200))

        layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)
      
        layout.addWidget(self.loading_text)
       

    def showEvent(self, event):
        self.loading_movie.start()

    def hideEvent(self, event):
        self.loading_movie.stop()
