import datetime
from attendance.models import Session, Attendance, Code
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
    institute_fnid = data["institute_fnid"]
    course_fnid = data["course_fnid"]
    session_type_fnid = data["session_type_fnid"]

    sessions = Session.objects.filter(institute_fnid=institute_fnid, course_fnid=course_fnid, session_type_fnid=session_type_fnid)

    start_time = convert_string_to_datetime(query.get("start_time", None))
    print("Query string", query, start_time)

    if not start_time:
        start_time = get_session_start()
        tz = pytz.timezone(settings.TIME_ZONE)
        start_time = start_time.replace(tzinfo=tz)

    print("Start time", start_time)
    if sessions.exists():
        print("Hello, a session exists")
        session = None
        for s in sessions:
            # find there is a session between times
            potential_sessions = Session.objects.filter(session_start__range=(start_time, start_time + timedelta(hours=int(s.duration_hrs))))
            if len(potential_sessions) > 0:
                print("Found a session")
                session = potential_sessions[0]
                break
        if not session:
            session = create_session(data, start_time)

    else:
        # create first session
        session = create_session(data, start_time)

    return session