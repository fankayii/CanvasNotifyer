import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, 
                             QTextBrowser, QComboBox)

# Assuming the following imports based on your explanation
from models import Assignment
from database import _get_all_ass, _get_map

class AssignmentPage(QWidget):
    def __init__(self):
        super().__init__()
        self.assignments = self.load_assignments()
        self.initUI()

    def load_assignments(self):
        data = _get_all_ass()
        assignments = []
        for item in data:
            ass = Assignment(*item)  # Using argument unpacking to fill the Assignment object
            assignments.append(ass)
        return assignments
    
    def initUI(self):
        layout = QVBoxLayout()

        # Dropdown for course selection
        self.course_selector = QComboBox(self)
        course_map = _get_map()
        courses = list(course_map.values())
        self.course_selector.addItems(courses)
        self.course_selector.currentIndexChanged.connect(self.update_table)
        layout.addWidget(self.course_selector)

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for assignments...")
        self.search_bar.textChanged.connect(self.update_table)
        layout.addWidget(self.search_bar)

        # Table to display assignments
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Modify as needed
        self.table.setHorizontalHeaderLabels(["Assignment Name", "Due Date", "Points", "Score"])
        self.table.cellDoubleClicked.connect(self.show_details)
        layout.addWidget(self.table)

        # For displaying HTML
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
        
        # Filter assignments based on search bar and course selection
        filtered_assignments = [a for a in self.assignments if search_text in a.name.lower() and a.cid == selected_course_id]

        # Update the table
        self.table.setRowCount(len(filtered_assignments))
        for row, assignment in enumerate(filtered_assignments):
            self.table.setItem(row, 0, QTableWidgetItem(assignment.name))
            self.table.setItem(row, 1, QTableWidgetItem(assignment.due_date))
            self.table.setItem(row, 2, QTableWidgetItem(str(assignment.points)))
            self.table.setItem(row, 3, QTableWidgetItem(str(assignment.score)))
    def update_content(self):
        self.assignments = self.load_assignments()
        self.update_table()
    def show_details(self, row, column):
        # Get assignment from the clicked row (adjust logic if necessary)
        assignment = [a for a in self.assignments if self.table.item(row, 0).text() == a.name][0]
        self.text_browser.setHtml(assignment.content)


