import os
import canvasapi
from datetime import datetime, timedelta
from models import Course, Assignment, Announcement
from dateutil.parser import parse
from database import insert_ass, insert_course, insert_assignment_group,insert_ann
from dotenv import load_dotenv,set_key,find_dotenv
import requests
BASEURL = 'https://ubc.instructure.com'
def get_canvas_api(api_token=None):
    if not api_token:
        load_dotenv()
        api_token = os.environ.get('CANVAS_API_TOKEN')

    
    return canvasapi.Canvas(BASEURL, api_token)
def write_usr_id(uid):
    env_path = find_dotenv()
    if not env_path:
        env_path = 'canvas notifyer/.env'
    set_key(env_path, 'USR_ID', uid)
    load_dotenv(env_path)

def _read_usr_id(api_token=None):
    load_dotenv(find_dotenv())
    uid = os.environ.get('USR_ID')
  
    if not uid:
        uid = _get_usr_id()
        write_usr_id(str(uid)) 
    return int(uid)


def _is_valid_token(api_token):
    try:
        canvas_api = canvasapi.Canvas(BASEURL, api_token)
        canvas_api.get_current_user()
        return True
    except Exception as e:
        return False
def _get_usr_name():
    canvas_api = get_canvas_api()
    return canvas_api.get_current_user().name

def _get_crse_name(cid):
    canvas_api = get_canvas_api()
    return canvas_api.get_course(cid).name

def _get_usr_id():
    canvas_api = get_canvas_api()
    return canvas_api.get_current_user().id

def _get_active_courses():
    """ Fetch the active course list
    """
    canvas_api = get_canvas_api()
    courses = [c for c in canvas_api.get_courses() if hasattr(c, 'enrollment_term_id')]
    return courses

def _print_ann(ann):
    for a in ann:
        print(a.title+" "+a.message+" "+a.posted_at)

def _get_curr_courses(flag):
    crse = [c.enrollment_term_id for c in _get_active_courses()]
    raw_courses = [c for c in _get_active_courses() if c.enrollment_term_id == max(crse)]
    

    
    if flag:
        test = [f"course_{r.id}" for r in raw_courses]

        for i in test:
      
            _get_annouce([i])


    courses = []
    for raw_course in raw_courses:
        course = Course(course_id=raw_course.id, course_name=raw_course.name)
        courses.append(course)
    _write_crse2db(courses)
    return courses
def _get_annouce(crses):
    canvas_api = get_canvas_api()
    raw = canvas_api.get_announcements(context_codes=crses)
    for a in raw:
        ann = Announcement(id=a.id,cid=crses[0].replace("course_",""),title=a.title,msg=a.message,date=a.posted_at)
        insert_ann(ann)

def _get_ass_re(crses):
    canvas_api = get_canvas_api()
    all_assignments = {}

    for crse in crses:
       
        raw_assignments = [a for a in canvas_api.get_course(crse.course_id).get_assignments() if a.due_at is not None]
        assignment_groups = [g for g in canvas_api.get_course(crse.course_id).get_assignment_groups()]

        for group in assignment_groups:
            insert_assignment_group(crse.course_id, group.id, group.name, group.group_weight)
 
        assignments = []
        for raw_assignment in raw_assignments:
          
            assignment = Assignment(id= raw_assignment.id, cid = crse.course_id ,name=raw_assignment.name, due_date=raw_assignment.due_at, points=raw_assignment.points_possible,
                                    is_submitted=_is_submit(raw_assignment),gid=raw_assignment.assignment_group_id,score=_get_score(raw_assignment))
            assignments.append(assignment)

       
        sorted_assignments = sorted(assignments, key=lambda x: x.due_date)
        
        all_assignments[crse.course_id] = sorted_assignments

    return all_assignments

def refresh_data(crses):
    all_assignments = _get_ass_re(crses)
    
    for crse_id, assignments in all_assignments.items():
        for assignment in assignments:
            insert_ass(assignment)

def _get_score(ass):
    submission = ass.get_submission(_read_usr_id())
    score = getattr(submission, 'score', None)
    return score if score is not None else -1



def _get_ass(crses):
    canvas_api = get_canvas_api()
    all_assignments = {}

    for crse in crses:
       
        raw_assignments = [a for a in canvas_api.get_course(crse.course_id).get_assignments() if a.due_at is not None]
        assignment_groups = [g for g in canvas_api.get_course(crse.course_id).get_assignment_groups() ]
        for group in assignment_groups:
            insert_assignment_group(crse.course_id, group.id, group.name, group.group_weight)

  
        assignments = []
        for raw_assignment in raw_assignments:
          
            assignment = Assignment(id= raw_assignment.id, cid = crse.course_id ,name=raw_assignment.name, due_date=raw_assignment.due_at, points=raw_assignment.points_possible,
                                    is_submitted=_is_submit(raw_assignment),gid=raw_assignment.assignment_group_id,score=_get_score(raw_assignment),content=raw_assignment.description)
            assignments.append(assignment)


        sorted_assignments = sorted(assignments, key=lambda x: x.due_date)
        
        all_assignments[crse.course_id] = sorted_assignments
    _write_ass2db(all_assignments)
    return all_assignments
def _write_crse2db(crse):
    for c in crse:
        insert_course(c)
def _write_ass2db(ass):
    for _, assignments in ass.items():
        for assignment in assignments:
            insert_ass(assignment)
  


def _get_usr_avatar():
    canvas_api = get_canvas_api()
    return canvas_api.get_current_user().avatar_url

   
def _sort_ass(ass):
    """Sort the assignment from nearest to furthest
    """
    return sorted(ass, key=lambda x: x.due_at)


def _get_ass_due_next_week(crses):
    assignments_dict = _get_ass(crses)  # Assuming _get_ass() returns a dictionary
    assignments_due_next_week = {}  # Dictionary to store assignments due next week

    

    for course_name, assignments in assignments_dict.items():
        assignments_due_next_week[course_name] = assignments  # Add them to the dictionary

    return assignments_due_next_week




def _is_submit(ass):
    submission = ass.get_submission(_get_usr_id())
    return submission.submitted_at!=None