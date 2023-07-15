from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from course.serializers import CourseSerializer, CourseInstanceStudentSerializer, CourseInstanceSerializer
from rest_framework.permissions import IsAuthenticated
from course.models import Course, CourseInstanceStudent, CourseInstance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from institute.models import InstituteConfig
import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from helpers.token_params import *
from drf_yasg.utils import swagger_auto_schema
import helpers.filters
from programme.models import Programme
from student.models import Student
from institute.models import Term





def get_start_date_from_week(fnid):
    institute_config = InstituteConfig.objects.get(institute_fnid=fnid)
    year = datetime.datetime.now().strftime("%Y")
    week = institute_config.term_start_week
    d = "{}-W{}".format(str(year), str(week))
    date = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    return date


class ListCreateCourseAPIView(ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid", "institute_fnid", "code", "name", "visible"]


    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = Course.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid"]


    def get_queryset(self):
        queryset = Course.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")


class ListCreateCourseInstanceStudentAPIView(ListCreateAPIView):
    serializer_class = CourseInstanceStudentSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid", "student_fnid"]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = CourseInstanceStudent.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        ])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CourseStudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseInstanceStudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid", "student_fnid"]


    def get_queryset(self):

        queryset = CourseInstanceStudent.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnide not supplied in query string.")


class ListCreateCourseInstanceAPIView(ListCreateAPIView):
    serializer_class = CourseInstanceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]


    def perform_create(self, serializer):
        start = serializer.validated_data.get("start", False)
        if not start:
            institute_fnid = self.request.query_params.get("institute_fnid", None)
            if institute_fnid:
                return serializer.save()

        return serializer.save()

    def get_queryset(self):
        #term_filter = helpers.filters.build_filter_from_query_string(self.request, Term)

        
        course_filter = helpers.filters.build_filter_from_query_string(self.request, Course)
        print("course queryset: ", course_filter)
        course_list = [x.fnid for x in Course.objects.filter(course_filter)]
        queryset_from_course = CourseInstance.objects.filter(course_fnid__in=course_list)

        try:
            instance_filter = helpers.filters.build_filter_from_query_string(self.request, CourseInstance)
            print("instance queryset: ", instance_filter)
            instance_queryset = CourseInstance.objects.filter(instance_filter)
        except:
            raise exceptions.ParseError("term_fnid UUID not valid.")
        
        
        #Combine the querysets
        queryset = instance_queryset | queryset_from_course

        if self.request.query_params.get("programme_name", None):
            programme_filter = helpers.filters.build_filter_from_query_string(self.request, Programme)
            programme_list = [x.fnid for x in Programme.objects.filter(programme_filter)]
            students = Student.objects.filter(programme_fnid__in=programme_list)
            students_list = [x.fnid for x in students]
            course_instance_list = [x.course_instance_fnid for x in CourseInstanceStudent.objects.filter(student_fnid__in=students_list)]
            queryset_from_programme = CourseInstance.objects.filter(fnid__in=course_instance_list)
            queryset = queryset | queryset_from_programme

        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        token_param_name,
        token_param_code,
        token_param_term,
        token_param_programme_name
        ])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CourseInstanceDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseInstanceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid", "course_fnid"]


    def get_queryset(self):

        queryset = CourseInstance.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")