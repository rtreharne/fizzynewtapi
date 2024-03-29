from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from attendance.serializers import SessionRequestSerializer, SessionSerializer, AttendanceSerializer
from course.serializers import CourseInstanceSerializer
from course.models import CourseInstance
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from attendance.models import SessionRequest, Session, Attendance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from course.models import CourseInstanceStudent, GroupStudent
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
import helpers.service
from django.utils import timezone


class UpdateAverageAttendance(APIView):
    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_session,
                                            token_param_student,])
    def get(self, request):
        institute_fnid = request.query_params.get("institute_fnid", None)


        if institute_fnid:
            # if institute_fnid doesn't exist, return error
            try:
                institute = Institute.objects.get(fnid=institute_fnid)
            except:
                return Response({'error': 'Could not find institute'}, status=status.HTTP_400_BAD_REQUEST)
            
            session_fnid = request.query_params.get("session_fnid", None)
            student_fnid = request.query_params.get("student_fnid", None)

            if student_fnid:
                try:
                    student = Student.objects.get(fnid=student_fnid)
                except:
                    return Response({'error': 'Could not find student'}, status=status.HTTP_400_BAD_REQUEST)

            if session_fnid:
                try:
                    session = Session.objects.get(fnid=session_fnid, institute_fnid=institute_fnid)
                except:
                    return Response({'error': 'Could not find session'}, status=status.HTTP_400_BAD_REQUEST)
                
                course_instance_fnid = session.course_instance_fnid
                enrollments_filter = helpers.filters.build_filter_from_query_string(request, CourseInstanceStudent)
                print("enrollments_filter", enrollments_filter)
                enrollments = CourseInstanceStudent.objects.filter(course_instance_fnid=course_instance_fnid).filter(enrollments_filter)
                students = Student.objects.filter(fnid__in=[x.student_fnid for x in enrollments])
                session_fnids = [session.fnid for session in Session.objects.filter(cancelled=False, void=False)]
                attendance = Attendance.objects.filter(session_fnid__in=session_fnids)
                

                for enrollment in enrollments:    
                    enrollment.average_attend_pc = helpers.service.calculate_attendance(attendance.filter(student_fnid=enrollment.student_fnid, course_instance_fnid=course_instance_fnid))
                    enrollment.save()
        

                for student in students:
                    student.average_attend_pc = helpers.service.calculate_attendance(attendance.filter(student_fnid=student.fnid))
                    student.save()

                return Response({'success': True, 'message': 'Average attendance updated.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Session fnid not provided'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Could not find institute'}, status=status.HTTP_400_BAD_REQUEST)

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
            sessions = [session.fnid for session in Session.objects.filter(filters_session).filter(cancelled=False, void=False)]

            queryset = Attendance.objects.filter(filters_attendance).filter(session_fnid__in=sessions)

            average_attendance = helpers.service.calculate_attendance(queryset)

            return Response({'average_attendance': average_attendance}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Could not find institute'}, status=status.HTTP_400_BAD_REQUEST)


class ListCreateSessionRequestAPIView(ListCreateAPIView):
    serializer_class = SessionRequestSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object

    def get_queryset(self):

        before = self.request.query_params.get("before", None)
        print("before", before)

        institute_fnid = self.request.query_params.get("institute_fnid", None)
        filters = helpers.filters.build_filter_from_query_string(self.request, SessionRequest)
        print(filters)

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


    def perform_create(self, serializer):
        new_object = serializer.save()

        group_fnid=None

        if new_object.group_fnid:
            # get all students in group
            group_students = GroupStudent.objects.filter(group_fnid=new_object.group_fnid)
            class_list = CourseInstanceStudent.objects.filter(course_instance_fnid=new_object.course_instance_fnid).filter(student_fnid__in=[x.student_fnid for x in group_students])
            group_fnid = new_object.group_fnid
        else:
            # create records for all
            class_list = CourseInstanceStudent.objects.filter(course_instance_fnid=new_object.course_instance_fnid)

        for student in class_list:
            
            student_info = Student.objects.get(fnid=student.student_fnid)
            attendance = Attendance(
                institute_fnid=student_info.institute_fnid,
                school_fnid=student_info.school_fnid,
                programme_fnid = student_info.programme_fnid,
                course_instance_fnid=student.course_instance_fnid,
                session_fnid=new_object.fnid,
                student_fnid=student.student_fnid,
                session_type_fnid=new_object.session_type_fnid,
                group_fnid=group_fnid,
            )

            try:
                attendance.save()
            except:
                print("error saving attendance record")
        return new_object
    
    def get_queryset(self):

        institute_fnid = self.request.query_params.get("institute_fnid", None)

        if institute_fnid:
            student_fnid = self.request.query_params.get("student_fnid", None)

            school_fnid = self.request.query_params.get("school_fnid", None)
            
            programme_fnid = self.request.query_params.get("programme_fnid", None)

            course_instance_fnid = self.request.query_params.get("course_instance_fnid", None)

            check = [student_fnid, school_fnid, programme_fnid, course_instance_fnid]

            # remove None and "" from check
            check = [x for x in check if x]



            filters = helpers.filters.build_filter_from_query_string(self.request, Session)

            queryset = Session.objects.filter(filters)
            
            course_instances = []

            if school_fnid:
                # Get all attendance records for school
                attendance_records = Attendance.objects.filter(school_fnid=school_fnid)

                # Get all related session_fnids from attendance_records
                session_fnids = [x.session_fnid for x in attendance_records]

                queryset = queryset.filter(fnid__in=session_fnids)
            
            if programme_fnid:
                # Get all attendance records for programme
                attendance_records = Attendance.objects.filter(programme_fnid=programme_fnid)

                # Get all related session_fnids from attendance_records
                session_fnids = [x.session_fnid for x in attendance_records]
                
                queryset = queryset.filter(fnid__in=session_fnids)
            
            if student_fnid:
                # Get all attendance records for student
                attendance_records = Attendance.objects.filter(student_fnid=student_fnid)

                # Get all related session_fnids from attendance_records
                session_fnids = [x.session_fnid for x in attendance_records]

                queryset = queryset.filter(fnid__in=session_fnids)

            if course_instance_fnid:

                queryset = queryset.filter(course_instance_fnid=course_instance_fnid)
            
            print("sessions: ", len(queryset))

            return queryset
        else:
            return Response({'error': 'Institutue fnid not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[token_param_config,
                                            token_param_fnid,
                                            token_param_school,
                                            token_param_course_instance,
                                            token_param_programme,
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
