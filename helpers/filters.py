from django.db import models as dmodels
from datetime import datetime
import json
from attendance.models import Session, Attendance
from student.models import Student

def json_datetime_to_python(json_dt):
    try:
        return datetime.strptime(json_dt, "%Y-%m-%dT%H:%M:%S")
    except:
        return json_dt

def build_filter_from_query_string(request, model_class, expired_override=None, active_override=False):

    fields = [f.name for f in model_class._meta.get_fields()]

    print(model_class, fields)
    print("Hello")
    

    institute_fnid = request.query_params.get("institute_fnid", None)
    programme_fnid = request.query_params.get("programme_fnid", None)
    course_instance_fnid = request.query_params.get("course_instance_fnid", False)
    after = request.query_params.get("after", False)
    before = request.query_params.get("before", False)
    student_fnid = request.query_params.get("student_fnid", False)
    expired = request.query_params.get("expired", None)
    active = request.query_params.get("active", None)

    

    print("programme_fnid", programme_fnid)

    if active_override is not None:
        if active_override:
            active = "true"
        else:
            active = "false"

    if expired_override is not None:
        if expired_override:
            expired = "true"
        else:
            expired = "false"

    session_type_fnid = request.query_params.get("session_type_fnid", False)
    session_fnid = request.query_params.get("session_fnid", False)
    fnid = request.query_params.get("fnid", False)
    present = request.query_params.get("present", False)
    school_fnid = request.query_params.get("school_fnid", False)
    programme_fnid = request.query_params.get("programme_fnid", False)


    if institute_fnid and "institute_fnid" in fields:
        filters = dmodels.Q(institute_fnid=institute_fnid)

    if model_class == Session:

        if session_fnid:
            filters &= dmodels.Q(fnid=session_fnid)
        if before:
            filters &= dmodels.Q(session_start__lte=json_datetime_to_python(before))
        else:
            filters &= dmodels.Q(session_start__lte=datetime.now())
        if after:
            filters &= dmodels.Q(session_start__gte=json_datetime_to_python(after))

    if fnid and "fnid" in fields:
        filters &= dmodels.Q(fnid=fnid)
    if course_instance_fnid and "course_instance_fnid" in fields:
        filters &= dmodels.Q(course_instance_fnid=course_instance_fnid)

    
    if student_fnid and "student_fnid" in fields:
        filters &= dmodels.Q(student_fnid=student_fnid)
    if expired is not None and "expired" in fields:
        filters &= dmodels.Q(expired=json.loads(expired))
    if session_type_fnid and "session_type_fnid" in fields:
        filters &= dmodels.Q(session_type_fnid=session_type_fnid)
    if session_fnid and "session_id" in fields:
        filters &= dmodels.Q(session_fnid=session_fnid)
    if present and "present" in fields:
        filters &= dmodels.Q(present=json.loads(present))
    if school_fnid and "school_fnid" in fields:
        filters &= dmodels.Q(school_fnid=school_fnid)
    if programme_fnid and "programme_fnid" in fields:
        filters &= dmodels.Q(programme_fnid=programme_fnid)
    if active and "active" in fields:
        filters &= dmodels.Q(active=json.loads(active))

    return filters