from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from attendance.serializers import SessionRequestSerializer, SessionSerializer, AttendanceSerializer
from course.serializers import CourseInstanceSerializer
from course.models import CourseInstance
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from attendance.models import SessionRequest, Session, Attendance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from course.models import CourseInstanceStudent
from student.models import Student
from drf_yasg.utils import swagger_auto_schema
from institute.models import Institute
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg import openapi
from helpers.token_params import *
import helpers.filters
from helpers.filters import json_datetime_to_python

class AverageAttendance(APIView):

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_school,
                                            token_param_programme,
                                            token_param_course_instance,
                                            token_param_session,
                                            token_param_student,
                                            token_param_start,
                                            token_param_end,
                                            token_param_present,
                                            token_param_session_type])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)
        filters_session = helpers.filters.build_filter_from_query_string(request, Session)
        filters_attendance = helpers.filters.build_filter_from_query_string(request, Attendance)

        print("Filters: ", filters_session)
        print("Filters Attendance:", filters_attendance)

        if institute_fnid:
            sessions = [x.fnid for x in Session.objects.filter(filters_session)]
            print("sessions", len(sessions))
            queryset = Attendance.objects.filter(filters_attendance).filter(session_fnid__in=sessions)

            try:
                average_attendance = float('{0:5g}'.format((queryset.filter(present=True).count()/queryset.count())*100))
            except ZeroDivisionError:
                average_attendance = 0

            return Response({'average_attendance': average_attendance}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Could not find institute'}, status=status.HTTP_400_BAD_REQUEST)


class ListCreateSessionRequestAPIView(ListCreateAPIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid",
                        "institute_fnid",
                        "student_fnid",
                        "course_instance_fnid",
                        "expired"
                        ]

    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object

    def get_queryset(self):

        institute_fnid = self.request.query_params.get("institute_fnid", None)
        filters = helpers.filters.build_filter_from_query_string(self.request, SessionRequest)

        if institute_fnid:
            queryset = SessionRequest.objects.filter(filters)
            print("length of queryset", len(queryset))
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_fnid,
                                            token_param_course_instance,
                                            token_param_student,
                                            token_param_start,
                                            token_param_end,
                                            token_param_expired,
                                            token_param_session,
                                            token_param_session_type])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SessionRequestDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = SessionRequest.objects.filter(institute_fnid=institute_fnid)
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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

        # create records for all
        class_list = CourseInstanceStudent.objects.filter(course_instance_fnid=new_object.course_instance_fnid)
        for student in class_list:
            print("student: ", student.__dict__)
            student_info = Student.objects.get(fnid=student.student_fnid)
            print("Updating attendance table")
            attendance = Attendance(
                institute_fnid=student.institute_fnid,
                school_fnid=student_info.school_fnid,
                programme_fnid = student_info.programme_fnid,
                course_instance_fnid=student.course_instance_fnid,
                session_fnid=new_object.fnid,
                student_fnid=student.student_fnid,
                session_type_fnid=new_object.session_type_fnid
            )
            print("nearly there")
            try:
                attendance.save()
            except:
                print("error saving attendance record")
        return new_object

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_fnid,
                                            token_param_course_instance,
                                            token_param_student,
                                            token_param_start,
                                            token_param_end,
                                            token_param_expired,
                                            token_param_session_type])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



    def get_queryset(self):

        institute_fnid = self.request.query_params.get("institute_fnid", None)
        filters = helpers.filters.build_filter_from_query_string(self.request, Session)

        if institute_fnid:
            queryset = Session.objects.filter(filters)
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
            return queryset
            #queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        filters = helpers.filters.build_filter_from_query_string(self.request, Attendance)

        if institute_fnid:
            queryset = Attendance.objects.filter(filters)
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[token_param_fnid,
                                            token_param_config,
                                            token_param_school,
                                            token_param_course_instance,
                                            token_param_session,
                                            token_param_student,
                                            token_param_start,
                                            token_param_end,
                                            token_param_present,
                                            token_param_session_type])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AttendanceDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = Attendance.objects.filter(institute_fnid=institute_fnid)
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset


    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
