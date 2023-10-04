from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QTextBrowser
from database import _get_all_ann, _get_map
from models import Announcement

class AnnouncementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.announcements = self.load_announcements()
        self.initUI()

    def load_announcements(self):
        data = _get_all_ann()
        announcements = []
        for item in data:
            ann = Announcement(*item) 
            announcements.append(ann)
        return announcements

    def initUI(self):
        layout = QVBoxLayout()


        self.course_selector = QComboBox(self)
        course_map = _get_map()
        courses = list(course_map.values())
        self.course_selector.addItems(courses)
        self.course_selector.currentIndexChanged.connect(self.update_table)
        layout.addWidget(self.course_selector)


        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for announcements...")
        self.search_bar.textChanged.connect(self.update_table)
        layout.addWidget(self.search_bar)


        self.table = QTableWidget(self)
        self.table.setColumnCount(2)  
        self.table.setHorizontalHeaderLabels(["Announcement Title", "Date"])
        self.table.cellDoubleClicked.connect(self.show_details)
        layout.addWidget(self.table)


        self.text_browser = QTextBrowser(self)
        layout.addWidget(self.text_browser)

        self.setLayout(layout)
        self.update_table()

    def update_table(self):
        search_text = self.search_bar.text().lower()
        selected_course_name = self.course_selector.currentText()
        course_map = _get_map()
        if not course_map:
            return
        selected_course_id = [cid for cid, cname in course_map.items() if cname == selected_course_name][0]
        

        filtered_announcements = [a for a in self.announcements if search_text in a.title.lower() and a.cid == selected_course_id]

        self.table.setRowCount(len(filtered_announcements))
        for row, announcement in enumerate(filtered_announcements):
            self.table.setItem(row, 0, QTableWidgetItem(announcement.title))
            self.table.setItem(row, 1, QTableWidgetItem(announcement.date))
    def update_content(self):
        self.announcements = self.load_announcements()
        self.update_table()
    def show_details(self, row, column):

        announcement = [a for a in self.announcements if self.table.item(row, 0).text() == a.title][0]
        self.text_browser.setHtml(announcement.msg)

