# api_thread.py

from PyQt5.QtCore import QThread, pyqtSignal
from script import _get_usr_name, _get_curr_courses, _get_ass_due_next_week, refresh_data,_get_annouce      
from database import get_assignments_due_within_week, _get_map, _get_ann_by_cid,_get_ann_by_date
class APIThread(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.execute_database_task = True
        self.user_name = None
        self.courses = None
        self.ass = None
        self.ann = None

    def fetch_ass_from_canvas(self):
        self.courses = _get_curr_courses(True)
  
        self.ass = _get_ass_due_next_week(self.courses)
        
    def read_ass_from_db(self):
        self.cmap = _get_map()
        self.ass = get_assignments_due_within_week()
    
    def refresh(self):
        self.courses = _get_curr_courses(True)
        refresh_data(self.courses)

    def set_edt_false(self):
        self.execute_database_task = False



        
    
    def run(self):
        # Simulated API calls
        self.user_name = _get_usr_name()  # Replace with actual function call
        self.courses = _get_curr_courses(False)
   
    
        #self.courses = _get_curr_courses()  # Replace with actual function call
        #self.cmap = _get_map()
        #print(self.courses)
        #self.ass = _get_ass_due_next_week(self.courses)

        #self.ass = get_assignments_due_within_week()
      
      
        #self.ass = _get_ass_due_next_week(124825)
        #self.ass_sub = [_is_submit(x) for x in self.ass]
        

        if self.execute_database_task:
            self.read_ass_from_db()
        else:
       
            self.fetch_ass_from_canvas()
            self.read_ass_from_db()
        self.ann = _get_ann_by_date()
    
          
            

        self.finished.emit()

    
    

