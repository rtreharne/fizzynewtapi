from django.db import models as dmodels
from datetime import datetime
import json
from attendance.models import Session

def json_datetime_to_python(json_dt):
    try:
        return datetime.strptime(json_dt, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return json_dt

def build_filter_from_query_string(request, model_class):

    fields = [f.name for f in model_class._meta.get_fields()]

    institute_fnid = request.query_params.get("institute_fnid", None)
    course_instance_fnid = request.query_params.get("course_instance_fnid", False)
    after = request.query_params.get("after", False)
    before = request.query_params.get("before", False)
    student_fnid = request.query_params.get("student_fnid", False)
    expired = request.query_params.get("expired", False)
    session_type_fnid = request.query_params.get("session_type_fnid", False)
    session_fnid = request.query_params.get("session_fnid", False)
    fnid = request.query_params.get("fnid", False)
    present = request.query_params.get("present", False)
    school_fnid = request.query_params.get("school_fnid", False)




    if institute_fnid and "institute_fnid" in fields:
        filters = dmodels.Q(institute_fnid=institute_fnid)
    if model_class == Session:
        print("Looking for session")
        if session_fnid:
            filters = dmodels.Q(fnid=session_fnid)
    if fnid and "fnid" in fields:
        filters &= dmodels.Q(fnid=fnid)
    if course_instance_fnid and "course_instance_fnid" in fields:
        filters &= dmodels.Q(course_instance_fnid=course_instance_fnid)
    if after and "after" in fields:
        filters &= dmodels.Q(session_start__gt=json_datetime_to_python(after))
    if before and "before" in fields:
        filters &= dmodels.Q(session_start__lt=json_datetime_to_python(before))
    if student_fnid and "student_fnid" in fields:
        filters &= dmodels.Q(student_fnid=student_fnid)
    if expired and "expired" in fields:
        filters &= dmodels.Q(expired=json.loads(expired))
    if session_type_fnid and "session_type_fnid" in fields:
        filters &= dmodels.Q(session_type_fnid=session_type_fnid)
    if session_fnid and "session_id" in fields:
        filters &= dmodels.Q(session_fnid=session_fnid)
    if present and "present" in fields:
        filters &= dmodels.Q(present=json.loads(present))
    if school_fnid and "school_fnid" in fields:
        filters &= dmodels.Q(school_fnid=school_fnid)

    return filters