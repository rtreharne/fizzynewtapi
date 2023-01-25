from django.db import models as dmodels
from datetime import datetime
import json

def json_datetime_to_python(json_dt):
    try:
        return datetime.strptime(json_dt, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return json_dt

def build_filter_from_query_string(request):
    institute_fnid = request.query_params.get("institute_fnid", None)
    course_instance_fnid = request.query_params.get("course_instance_fnid", False)
    after = request.query_params.get("after", False)
    before = request.query_params.get("before", False)
    student_fnid = request.query_params.get("student_fnid", False)
    expired = request.query_params.get("expired", False)
    session_type_fnid = request.query_params.get("session_type_fnid", False)
    session_fnid = request.query_params.get("session_fnid", False)

    if institute_fnid:
        filters = dmodels.Q(institute_fnid=institute_fnid)
    if course_instance_fnid:
        filters &= dmodels.Q(course_instance_fnid=course_instance_fnid)
    if after:
        filters &= dmodels.Q(session_start__gt=json_datetime_to_python(after))
    if before:
        filters &= dmodels.Q(session_start__lt=json_datetime_to_python(before))
    if student_fnid:
        filters &= dmodels.Q(student_fnid=student_fnid)
    if expired:
        filters &= dmodels.Q(expired=json.loads(expired))
    if session_type_fnid:
        filters &= dmodels.Q(session_type_fnid=session_type_fnid)
    if session_fnid:
        filters &= dmodels.Q(session_fnid=session_fnid)

    return filters