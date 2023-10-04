import sqlite3
from datetime import datetime, timedelta

def create_tables():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    # create table for courses
    c.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL
    );
    ''')

    # create table for assignments
    c.execute('''
    CREATE TABLE IF NOT EXISTS assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        name TEXT,
        due_date TEXT,
        points INTEGER,
        is_submitted BOOLEAN,
        group_id INTEGER,
        score INTEGER,
        content TEXT,
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
    );
    ''')

    # create table for assignment group
    c.execute('''
        CREATE TABLE IF NOT EXISTS assignment_groups (
            group_id INTEGER PRIMARY KEY,
            course_id INTEGER,
            name TEXT,
            weight REAL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        );
    ''')
    
    # create table for annoucement
    c.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            title TEXT,
            message TEXT,
            date TEXT,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        );
    ''')

    conn.commit()
    conn.close()
def insert_ann(ann):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    INSERT OR IGNORE INTO announcements (announcement_id, course_id, title, message, date) 
    VALUES (?, ?, ?, ?, ?)""",
    (ann.id, ann.cid, ann.title, ann.msg, ann.date))

    c.execute("""
        UPDATE announcements SET 
        course_id = ?, 
        title = ?, 
        message = ?, 
        date = ?
        WHERE announcement_id = ?  -- Corrected column name
    """, (ann.cid, ann.title, ann.msg, ann.date, ann.id))


    conn.commit()
    conn.close()

       

def insert_course(crse):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    # Use "INSERT OR REPLACE" to either insert a new row or replace the existing one
    c.execute("INSERT OR REPLACE INTO courses (course_id, course_name) VALUES (?, ?)", (crse.course_id, crse.course_name,))
    
    conn.commit()
    conn.close()

def insert_assignment_group(course_id, group_id, name, weight):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO assignment_groups (group_id, course_id, name, weight) VALUES (?, ?, ?, ?)",
              (group_id, course_id, name, weight))
    conn.commit()
    conn.close()

def insert_ass(assignment):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

   
    c.execute("""
        INSERT OR IGNORE INTO assignments 
        (assignment_id, course_id, name, due_date, points, is_submitted, group_id, score, content) 
        VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
    """, (assignment.id, assignment.cid, assignment.name, assignment.due_date, assignment.points, assignment.is_submitted, assignment.gid,assignment.score,assignment.content))

    # Step 2: Update the record if it already existed
    c.execute("""
    UPDATE assignments SET 
    course_id = ?, 
    name = ?, 
    due_date = ?, 
    points = ?, 
    is_submitted = ?, 
    group_id = ?,
    score = ?,
    content = ?
    WHERE assignment_id = ?
""", (assignment.cid, assignment.name, assignment.due_date, assignment.points, assignment.is_submitted, assignment.gid, assignment.score,assignment.content, assignment.id))

    
    conn.commit()
    conn.close()


def _get_map():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    course_id_to_name = {}
    c.execute("SELECT course_id, course_name FROM courses")
    for row in c.fetchall():
        course_id, course_name = row
        course_id_to_name[course_id] = course_name
    conn.close()
    return course_id_to_name


def get_assignments_due_within_week():

    conn = sqlite3.connect("data.db")
    c = conn.cursor()



   
    

    # Get the current date and time in ISO 8601 format (matching SQLite)
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Calculate the date and time one week from now
    one_week_from_now = (datetime.utcnow() + timedelta(weeks=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Execute SQL query to find assignments due within the week
    c.execute("SELECT * FROM assignments WHERE due_date >= ? AND due_date <= ?", (now, one_week_from_now))

    # Fetch all matching records
    records = c.fetchall()

    conn.close()
    return records
def _get_all_ass():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM assignments")
    ass = c.fetchall()
    conn.close()
    return ass

def _get_ann_by_cid(cid):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    c.execute("SELECT announcement_id, course_id, title, message, date FROM announcements WHERE course_id=?", (cid,))
    
    announcements = c.fetchall()
    conn.close()

    return announcements
def _get_all_ann():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM  announcements")
    ann = c.fetchall()
    
    conn.close()
    return ann
def _get_ann_by_date():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()



   
    

    # Get the current date and time in ISO 8601 format (matching SQLite)
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Calculate the date and time one week from now
    one_week_from_now = (datetime.utcnow() - timedelta(weeks=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Execute SQL query to find assignments due within the week
    c.execute("SELECT announcement_id, course_id, title, message, date FROM announcements WHERE date >= ? AND date <= ?", (one_week_from_now,now))

    announcements = c.fetchall()
    conn.close()

    return announcements


create_tables()
    


