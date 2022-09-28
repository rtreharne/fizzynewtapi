import datetime
from attendance.models import Session, Attendance, Code
from course.models import Course, CourseInstanceStudent
from student.models import Student
from django.conf import settings
import pytz
from datetime import timedelta
import random


def get_session_start():
    now = datetime.datetime.now()
    now_min = now.minute
    if now_min >= 15:
        dt = 30 - now_min
        if now_min >= 30:
            dt = 30 - now_min
            if now_min >= 45:
                dt = 60 - now_min
    else:
        dt = - now_min

    session_time = now + datetime.timedelta(minutes=dt)
    session_time = session_time.replace(second=0, microsecond=0)

    return session_time

def get_random_code():
    items = list(Code.objects.all())
    return random.choice(items).code

def get_random_codes(n):
    items = list(Code.objects.all())
    return random.sample(items, n)

def create_session(data, start_time):
    session = Session(
        session_type_fnid= data["session_type_fnid"],
        institute_fnid= data["institute_fnid"],
        course_fnid= data["course_fnid"],
        session_code= get_random_code(),
        session_start=start_time
    )
    session.save()
    return session

def convert_string_to_datetime(string):
    if string:
        dt = datetime.datetime.strptime(string, "%Y%m%dT%H%M")
        tz = pytz.timezone(settings.TIME_ZONE)
        dt = dt.replace(tzinfo=tz)
        return dt

def check_for_session(data, query):
    # get session infor from query string
    institute_fnid = data["institute_fnid"]
    course_fnid = data["course_fnid"]
    session_type_fnid = data["session_type_fnid"]
    student_fnid = data["student_fnid"]

    # get existing sessions
    sessions = Session.objects.filter(institute_fnid=institute_fnid, course_fnid=course_fnid, session_type_fnid=session_type_fnid)

    # get start_time from query string and convert to django tz datetime
    start_time = convert_string_to_datetime(query.get("start_time", None))

    if not start_time: # if start_time not supplied in query string
        start_time = get_session_start() # Get nearest session start time

        # convert start_time to tz datetime
        tz = pytz.timezone(settings.TIME_ZONE)
        start_time = start_time.replace(tzinfo=tz)

    if sessions.exists():

        session = None
        for s in sessions:
            # find there is a session between times
            potential_sessions = Session.objects.filter(session_start__range=(start_time, start_time + timedelta(hours=int(s.duration_hrs))))
            if len(potential_sessions) > 0:
                session = potential_sessions[0]

                attendance_records = Attendance.objects.filter(session_fnid=session.fnid)
                course = Course.objects.get(fnid=course_fnid)

                # mark student present
                attendance_record = attendance_records.get(student_fnid=student_fnid)
                attendance_record.present = True
                attendance_record.save()

                # update session attendance score

                marked_present = len(attendance_records.filter(present=True))
                attendance_pc = marked_present*100/len(attendance_records)
                session.average_attendance = round(attendance_pc, 1)

                # update session confirmed
                if attendance_pc >= course.threshold:
                    session.confirmed = True

                session.save()


                break
        if not session:
            session = create_session(data, start_time)
            create_attendance_log_for_session(data, query, session)

    else:
        # create first session
        session = create_session(data, start_time)
        print("Creating first session log")
        create_attendance_log_for_session(data, query, session)

    return session

def create_attendance_log_for_session(data, query, session):

    print("starting create_attendance_log")

    institute_fnid = data["institute_fnid"]
    school_fnid = data["school_fnid"]
    student_fnid = data["student_fnid"]
    session_type_fnid = data["session_type_fnid"]

    # get all students on course
    course_fnid = data["course_fnid"]
    student_ids = [x.student_fnid for x in CourseInstanceStudent.objects.filter(course_fnid=course_fnid)]

    # get random selection of codes. ALL UNIQUE!
    codes = get_random_codes(len(student_ids))

    # create attendance records
    for student, code in zip(student_ids, codes):
        record = Attendance(
            institute_fnid=institute_fnid,
            school_fnid=school_fnid,
            course_fnid=course_fnid,
            session_fnid=session.fnid,
            session_type_fnid=session_type_fnid,
            student_fnid=student,
            session_code=session.session_code,
            student_code=code
        )
        # if triggered by student mark them as present
        if student == student_fnid:
            record.present = True

        record.save()


