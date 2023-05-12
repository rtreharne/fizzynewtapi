from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from student.models import Student
from course.models import Course, CourseInstanceStudent
from attendance.models import SessionRequest
from institute.models import Institute
from attendance.models import Session, Attendance
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from attendance.serializers import SessionRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from helpers.token_params import *
import helpers.filters


class ActiveSession(APIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_school,
                                            token_param_course_instance,
                                            token_param_start,
                                            token_param_end,
                                            token_param_present,
                                            token_param_session_type,
                                            token_param_programme
                                            ])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)

        # Get school_fnid if in query string
        school_fnid = request.query_params.get("school_fnid", None)

        # Get course_instance_fnid if in query string
        course_instance_fnid = request.query_params.get("course_instance_fnid", None)

        # Get programme_fnid if in query string
        programme_fnid = request.query_params.get("programme_fnid", None)

        # Get all ongoing sessions
        filters_session = helpers.filters.build_filter_from_query_string(request, Session, expired_override=False)

        if institute_fnid:
            sessions = [x.fnid for x in Session.objects.filter(filters_session)]

            # Get all attendance records associated with ongoing sessions
            attendance_records_all = Attendance.objects.filter(session_fnid__in=sessions)

            # Get all attendance records associated with ongoing sessions where students are present
            attendance_records_present = attendance_records_all.filter(present=True)

            # Calculate attendance percentage
            total_students = len(attendance_records_all)
            attending_students = len(attendance_records_present)
            if total_students != 0:
                attendance_percentage = (attending_students / total_students) * 100
            else:
                attendance_percentage = 0

            # Build JSON response data
            data = {
                "institute_fnid": institute_fnid,
                "school_fnid": school_fnid,
                "programme_fnid": programme_fnid,
                "course_instance_fnid": course_instance_fnid,
                "sessions_count": len(sessions),
                "total_students": total_students,
                "attending_students": attending_students,
                "attending_percentage": "{:.1f}".format(attendance_percentage)
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)




