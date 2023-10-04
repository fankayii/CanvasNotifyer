from PyQt5.QtWidgets import  QStackedWidget, QVBoxLayout, QPushButton, QToolBox, QLabel, QCheckBox
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QToolBox, QToolButton, QHBoxLayout,QCheckBox,QPushButton
from PyQt5.QtGui import QMovie, QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt, QSize
from api_thread import APIThread  # Import the APIThread class
from script import _get_crse_name
from loading_widget import LoadingWidget
from models import AnnouncementDialog
from ass_page import AssignmentPage
from ann_page import AnnouncementPage


class MainAppPage(QWidget):
    data_fetched = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.checkboxes = []
        self.announ = []
        self.userflag = False
        
        self.loading_widget = LoadingWidget()
        self.initUI()

        self.db_api_thread = APIThread()
        self.db_api_thread.finished.connect(self.on_data_fetched)
        self.loading_widget.show()
        self.db_api_thread.start()

    def initUI(self):
        self.top_layout = QVBoxLayout(self)

        # Button to toggle the sidebar's visibility
        self.sidebar_button = QPushButton('☰')
        self.sidebar_button.clicked.connect(self.toggle_sidebar)
        self.top_layout.addWidget(self.sidebar_button)

        # Main layout as a QHBoxLayout
        self.layout = QHBoxLayout()
        self.top_layout.addLayout(self.layout)
        
        # Sidebar: QToolBox for navigation
        self.sidebar = QToolBox()
        self.layout.addWidget(self.sidebar)  # Add to main layout

        # Stacked Widget: For content pages
        self.main_content = QStackedWidget()
        self.layout.addWidget(self.main_content)

        # Default page in sidebar and content area
        self.default_page = QWidget()
        self.default_layout = QVBoxLayout(self.default_page)
        self.sidebar.addItem(self.default_page, "Default")
        self.main_content.addWidget(self.default_page)

        # Assignments page in sidebar and content area
        self.assignments_page = AssignmentPage()
        self.sidebar.addItem(self.assignments_page, "Assignments")
        self.data_fetched.connect(self.assignments_page.update_content)
        self.main_content.addWidget(self.assignments_page)

        # Announcements page in sidebar and content area
        self.announcements_page = AnnouncementPage()
        self.sidebar.addItem(self.announcements_page, "Announcements")
        self.data_fetched.connect(self.announcements_page.update_content)
        self.main_content.addWidget(self.announcements_page)

        # Connect the QToolBox currentChanged signal to change the content area
        self.sidebar.currentChanged.connect(self.change_main_content)
        self.sidebar.currentChanged.connect(self.refresh_page)

        # Refresh button (you can adjust its placement as needed)
        self.refre = QPushButton("refresh")
        self.refre.clicked.connect(self.on_submit)
        self.default_layout.addWidget(self.refre)
        self.refre.hide()

        self.setLayout(self.top_layout)
    def refresh_page(self, index):
        if index == 0:  # Assuming 0 is the index for the Default page
            # Logic to refresh and load content for the Default page
            self.on_data_fetched()

    def change_main_content(self, index):
    # Set the current index of the main_content (QStackedWidget) 
    # to match the current index of the sidebar (QToolBox)
        self.main_content.setCurrentIndex(index)
    def toggle_sidebar(self):
        # Toggle visibility of the sidebar
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def on_data_fetched(self):
        self.loading_widget.hide()
        self.refre.show()

        if not self.userflag:
            user_name = self.db_api_thread.user_name  # Assuming you set this in your thread
            self.name_label = QLabel("Hello: " + user_name)
            self.default_layout.addWidget(self.name_label)
            self.userflag = True

        crse_map = self.db_api_thread.cmap
        ass = self.db_api_thread.ass
        ann = self.db_api_thread.ann
        for an in self.announ:
            an.deleteLater()
        self.announ.clear()
        for an in ann:
            title_label = QPushButton(an[2])  # Using QPushButton so it can be clicked
            title_label.setToolTip(f"Date: {an[4]}")
            title_label.clicked.connect(lambda checked, an=an: self.show_ann(an))
            self.default_layout.addWidget(title_label)  # Add to the default page layout
            self.announ.append(title_label)

        for cb in self.checkboxes:
            cb.deleteLater()
        self.checkboxes.clear()

        for a in ass:
            checkbox = QCheckBox(f"{crse_map.get(a[1])[:8]} {a[2]} (Due: {a[3]})")  # Indexes based on your tuple structure
            checkbox.setChecked(a[5])  # Assuming is_submitted is at index 5 in the tuple
            self.default_layout.addWidget(checkbox)  # Add to the default page layout
            self.checkboxes.append(checkbox)


    def show_ann(self, ann):
        announcement_title = ann[2]  # Assuming title is in the 3rd position
        announcement_msg = ann[3]    # Assuming message is in the 4th position
        dialog = AnnouncementDialog(announcement_title, announcement_msg, self)
        dialog.exec_()

    def on_submit(self):
        self.db_api_thread = APIThread()
        self.db_api_thread.execute_database_task = False
        
        self.db_api_thread.finished.connect(self.on_data_fetched)
        self.loading_widget.show()
        self.db_api_thread.start()


