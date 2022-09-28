from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from student.models import Student
from course.models import Course, CourseInstanceStudent
from institute.models import Institute
from attendance.models import Session, Attendance
import datetime

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

