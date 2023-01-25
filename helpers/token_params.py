from drf_yasg import openapi
token_param_start = openapi.Parameter('after', in_=openapi.IN_QUERY, description="filter for session requests that started after this datetime", type=openapi.FORMAT_DATETIME)
token_param_end = openapi.Parameter('before', in_=openapi.IN_QUERY, description="filter for session requests that started before this datetime", type=openapi.FORMAT_DATETIME)
token_param_config = openapi.Parameter('institute_fnid', in_=openapi.IN_QUERY, description="This parameter must be included in the query string of every call.", type=openapi.TYPE_STRING)
token_param_student = openapi.Parameter('student_fnid', in_=openapi.IN_QUERY, description="filter for student_fnid", type=openapi.TYPE_STRING)
token_param_session_type = openapi.Parameter('session_type_fnid', in_=openapi.IN_QUERY, description="filter for session_type_fnid", type=openapi.TYPE_STRING)
token_param_session = openapi.Parameter('session_fnid', in_=openapi.IN_QUERY, description="filter for session_fnid", type=openapi.TYPE_STRING)
token_param_expired = openapi.Parameter('expired', in_=openapi.IN_QUERY, description="filter for expired course requests", type=openapi.TYPE_BOOLEAN)
token_param_course_instance=openapi.Parameter('course_instance_fnid', in_=openapi.IN_QUERY, description="filter for course_instance_fnid", type=openapi.TYPE_STRING)