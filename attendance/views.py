from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from attendance.serializers import SessionRequestSerializer, SessionSerializer, AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from attendance.models import SessionRequest, Session, Attendance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from course.models import CourseInstanceStudent
from student.models import Student

from django.conf import settings
import pytz
from institute.models import Institute
from datetime import timedelta


class ListCreateSessionRequestAPIView(ListCreateAPIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid",
                        "institute_fnid",
                        "student_fnid",
                        "course_instance_fnid",
                        ]

    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object

    def get_queryset(self):
        queryset = SessionRequest.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

class SessionRequestDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = SessionRequest.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset


class ListCreateSessionAPIView(ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid",
                        "institute_fnid",
                        "course_instance_fnid",
                        "session_start",
                        "session_audit",
                        ]

    def perform_create(self, serializer):
        new_object = serializer.save()

        # create records for all students
        print(new_object.__dict__)
        class_list = CourseInstanceStudent.objects.all()
        for student in class_list:
            print("student: ", student.__dict__)
            student_info = Student.objects.get(fnid=student.student_fnid)
            attendance = Attendance(
                institute_fnid=student.institute_fnid,
                school_fnid=student_info.school_fnid,
                course_instance_fnid=student.course_instance_fnid,
                session_fnid=new_object.fnid,
                student_fnid=student.student_fnid,
                session_type_fnid=new_object.session_type_fnid
            ).save()
            print(student_info.__dict__)
        return new_object



    def get_queryset(self):
        queryset = Session.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")


class SessionDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = Session.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset


class ListCreateAttendanceAPIView(ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid",
                        "institute_fnid",
                        "student_fnid",
                        "course_instance_fnid",
                        "session_fnid",
                        "session_type_fnid"
                        ]

    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object

    def get_queryset(self):
        queryset = Attendance.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")


class AttendanceDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid", "school_fnid", "course_instance_fnid",
                        "session_fnid", "student_fnid", "session_type_fnid"]

    def get_queryset(self):

        queryset = Attendance.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset



