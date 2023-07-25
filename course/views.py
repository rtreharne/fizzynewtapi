from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from course.serializers import CourseSerializer, CourseInstanceStudentSerializer, CourseInstanceSerializer, GroupSerializer, GroupStudentSerializer
from rest_framework.permissions import IsAuthenticated
from course.models import Course, CourseInstanceStudent, CourseInstance, Group, GroupStudent
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

        return queryset


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

        institute_fnid = self.request.query_params.get("institute_fnid", None)

        code = self.request.query_params.get("code", None)
        term_fnid = self.request.query_params.get("term_fnid", None)
        programme_name = self.request.query_params.get("programme_name", None)
        name = self.request.query_params.get("name", None)

        param_list = [code, term_fnid, programme_name, name]

        # Remove item from param_list if None or ""
        param_list = [x for x in param_list if x]

        print("param_list", param_list)
        if len(param_list) > 1:
            raise exceptions.ParseError("Only one of code, term_fnid, programme_name, name can be supplied in query string.")

        try:
            instance_filter = helpers.filters.build_filter_from_query_string(self.request, CourseInstance)
            instance_queryset = CourseInstance.objects.filter(instance_filter)
            if self.request.query_params.get("term_fnid", None):
                term_fnid = self.request.query_params.get("term_fnid", None)
                queryset = instance_queryset.filter(term_fnid=term_fnid)
            else:
                queryset = instance_queryset
        except:
            raise exceptions.ParseError("term_fnid UUID not valid.")
        
        
        if self.request.query_params.get("code", None):
            course_filter = helpers.filters.build_filter_from_query_string(self.request, Course)
            course_list = [x.fnid for x in Course.objects.filter(course_filter)]
            queryset_from_course = CourseInstance.objects.filter(institute_fnid=institute_fnid, course_fnid__in=course_list)
            queryset = queryset_from_course


        if self.request.query_params.get("programme_name", None):
            programme_list = [x.fnid for x in Programme.objects.filter(name__icontains=programme_name)]
            students = Student.objects.filter(institute_fnid=institute_fnid, programme_fnid__in=programme_list)
            students_list = [x.fnid for x in students]
            print("Students count:" , len(students))
            course_instance_list = [x.course_instance_fnid for x in CourseInstanceStudent.objects.filter(student_fnid__in=students_list)]
            queryset_from_programme = CourseInstance.objects.filter(institute_fnid=institute_fnid, fnid__in=course_instance_list)
            queryset = queryset_from_programme

        
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


class ListCreateGroupAPIView(ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]


    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):

        institute_fnid = self.request.query_params.get("institute_fnid", None)
        course_instance_fnid = self.request.query_params.get("course_instance_fnid", None)
        group_filter = helpers.filters.build_filter_from_query_string(self.request, Group)

        if institute_fnid:
            return Group.objects.filter(group_filter)
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        token_param_course_instance
        ])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GroupDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid", "course_instance_fnid"]


    def get_queryset(self):

        queryset = Group.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")


class ListCreateGroupStudentAPIView(ListCreateAPIView):
    serializer_class = GroupStudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]


    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):

        institute_fnid = self.request.query_params.get("institute_fnid", None)

        filter = helpers.filters.build_filter_from_query_string(self.request, GroupStudent)

        if institute_fnid:
            return GroupStudent.objects.filter(filter)
        else:
            raise exceptions.ParseError("institute_fnid  not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        token_param_group,
        ])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class GroupStudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GroupStudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid", "group_fnid"]

    def get_queryset(self):

        queryset = GroupStudent.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")
        
    @swagger_auto_schema(manual_parameters=[
        token_param_config,
        ])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
