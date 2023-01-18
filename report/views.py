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

token_param_start = openapi.Parameter('after', in_=openapi.IN_QUERY, description="filter for session requests that started after this datetime", type=openapi.FORMAT_DATETIME)
token_param_end = openapi.Parameter('before', in_=openapi.IN_QUERY, description="filter for session requests that started before this datetime", type=openapi.FORMAT_DATETIME)


def json_datetime_to_python(json_dt):
    try:
        return datetime.strptime(json_dt, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return json_dt

class ActiveSessionRequest(APIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)

    def filter_by_datetime(self, request, queryset):
        if request.GET.get("after", False):
            try:
                queryset = queryset.filter(session_start__gte=json_datetime_to_python(request.GET["after"]))
            except:
                pass

        if request.GET.get("before", False):
            try:
                queryset = queryset.filter(session_start__lte=json_datetime_to_python(request.GET["before"]))
            except:
                pass

        return queryset


    @swagger_auto_schema(manual_parameters=[token_param_start, token_param_end])
    def get(self, request, institute_fnid=None, student_fnid=None):


        try:
            institute = Institute.objects.get(fnid=institute_fnid)
        except:
            return Response({'error': 'Institute does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(fnid=student_fnid)
        except:
            return Response({'error': 'Student does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = SessionRequest.objects.filter(institute_fnid=institute_fnid, student_fnid=student_fnid)
        queryset = self.filter_by_datetime(request, queryset)

        serializer = SessionRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_student(student_fnid):
    student = Student.objects.get(fnid=student_fnid)
    return student

def get_student_enrollments(student_fnid):
    enrollments = CourseInstanceStudent.objects.filter(student_fnid=student_fnid)
    courses = [Course.objects.get(fnid=x.course_fnid) for x in enrollments]
    detail = [{

    }]
    return enrollments

class StudentSummaryReport(APIView):

    def get(self, request):

        response_data = {}
        institute_fnid = self.request.query_params.get("institute_fnid")
        student_fnid = self.request.query_params.get("student_fnid", None)

        if student_fnid:
            student = get_student(student_fnid)
            enrollments = get_student_enrollments(student_fnid)
            response_data["enrollments"] = [{"start_date": x.updated_at} for x in enrollments]


        return Response({'report_data': response_data}, status=status.HTTP_200_OK)

class StudentFullReport(APIView):

    def get(self, request):
        pass

