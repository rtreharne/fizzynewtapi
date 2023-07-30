from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from student.serializers import StudentSerializer, StudentEmailSerializer, StudentTermSerializer
from rest_framework.permissions import IsAuthenticated
from student.models import Student, StudentEmail, StudentTerm
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from helpers.token_params import *
import helpers.filters
from course.models import CourseInstanceStudent
from attendance.models import Session, Attendance
from datetime import datetime
from django.utils import timezone
from django.db import models as dmodels


class ListCreateStudentAPIView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]


    def perform_create(self, serializer):
        serializer.is_valid()
        return serializer.save()

    def get_queryset(self):

        filters_student = helpers.filters.build_filter_from_query_string(self.request, Student)

        if self.request.query_params.get("course_instance_fnid", None):
            course_instance_fnid = self.request.query_params.get("course_instance_fnid", None)
            enrollments = CourseInstanceStudent.objects.filter(course_instance_fnid=course_instance_fnid)
            student_fnids = {enrollment.student_fnid: enrollment.average_attend_pc for enrollment in enrollments}
            filters_student &= dmodels.Q(fnid__in=list(student_fnids.keys()))
            queryset = Student.objects.all().filter(filters_student)

        else:
            queryset = Student.objects.all().filter(filters_student)

        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        token_param_school,
        token_param_programme,
        token_param_last_name,
        token_param_first_name,
        token_param_active,
        token_param_international,
        token_param_course_instance,
        token_param_min,
        token_param_max,
        token_param_student_id,
        ])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class StudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        queryset = Student.objects.all()
        return queryset

class ListCreateStudentEmailAPIView(ListCreateAPIView):
    serializer_class = StudentEmailSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["fnid", "institute_fnid", "student_fnid", "primary", "email"]

    def perform_create(self, serializer):
        serializer.is_valid()

        # Set primary field to False for all existing student emails if new email is primary
        existing_emails = StudentEmail.objects.filter(student_fnid=serializer.validated_data["student_fnid"])
        if serializer.validated_data.get("primary", False):

            if len(existing_emails) > 0:
                existing_emails.update(primary=False)

        elif len(existing_emails) == 0:
            return serializer.save(primary=True)

        return serializer.save()

    def get_queryset(self):
        queryset = StudentEmail.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")


class StudentEmailDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentEmailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):
        return Student.objects.all()

class ListCreateStudentTermAPIView(ListCreateAPIView):
    serializer_class = StudentTermSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["fnid", "institute_fnid", "student_fnid", "term_fnid", "current"]

    def perform_create(self, serializer):
        serializer.is_valid()
        return serializer.save()

    def get_queryset(self):
        institute_fnid = self.request.query_params.get("institute_fnid", None)

        if institute_fnid:
            filters = helpers.filters.build_filter_from_query_string(self.request, StudentTerm)
            print("STUDENT TERM FILTER: ", filters)

            queryset = StudentTerm.objects.filter(filters)

            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")
    
    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        token_param_student,
        ])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentTermDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentTermSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = StudentTerm.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")