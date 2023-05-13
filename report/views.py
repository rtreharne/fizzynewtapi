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


class AttendanceOverview(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_school,
                                            token_param_course_instance,
                                            token_param_programme,
                                            token_param_min,
                                            token_param_max
                                            ])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)

        # Get school_fnid if in query string
        school_fnid = request.query_params.get("school_fnid", None)

        # Get course_instance_fnid if in query string
        course_instance_fnid = request.query_params.get("course_instance_fnid", None)

        # Get programme_fnid if in query string
        programme_fnid = request.query_params.get("programme_fnid", None)

        # Get min value from query string
        min_value = request.query_params.get("min", None)

        # Get max value if in query string
        max_value = request.query_params.get("max", None)

        # Get all active students
        filters_student = helpers.filters.build_filter_from_query_string(request, Student, active_override=True)

        if institute_fnid and min_value:
            students = [x.fnid for x in Student.objects.filter(filters_student)]

            # Get all attendance records associated with ongoing sessions
            active_students_all = Student.objects.filter(fnid__in=students)

            # Get all attendance records associated with ongoing sessions where students are present
            if max_value is None:
                new_max=101
            else:
                new_max=max_value

            active_students_band = active_students_all.filter(average_attend_pc__gte=min_value, average_attend_pc__lt=new_max)

            # Calculate band attendance percentage
            total_students = len(active_students_all)
            students_in_band = len(active_students_band)
            if total_students != 0:
                band_percentage = (students_in_band / total_students) * 100
            else:
                band_percentage = 0

            # Build JSON response data
            data = {
                "institute_fnid": institute_fnid,
                "school_fnid": school_fnid,
                "programme_fnid": programme_fnid,
                "course_instance_fnid": course_instance_fnid,
                "total_students": total_students,
                "students_in_band": students_in_band,
                "percentage": "{:.1f}".format(band_percentage),
                "min": min_value,
                "max": max_value
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)



