# models.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser
class Assignment:
    def __init__(self, id,cid,name, due_date, points,is_submitted, gid,score,content):
        self.id = id  # ass id
        self.cid = cid # course id
        self.name = name 
        self.due_date = due_date
        self.points = points
        self.is_submitted = is_submitted
        self.gid = gid # assignment_group_id
        self.score = score
        self.content = content # ass detail
    


class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name
        self.assignments = []  # List to store Assignment objects

    def add_assignment(self, assignment):
        self.assignments.append(assignment)



class Announcement:
    def __init__(self,id,cid,title,msg,date):
        self.id = id
        self.cid = cid
        self.title = title
        self.msg = msg
        self.date = date

class AnnouncementDialog(QDialog):
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(title)
        layout = QVBoxLayout()

        self.content_browser = QTextBrowser()
        self.content_browser.setHtml(content)
        layout.addWidget(self.content_browser)
        self.setLayout(layout)