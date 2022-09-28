from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from course.serializers import CourseSerializer, CourseInstanceStudentSerializer, CourseInstanceSerializer
from rest_framework.permissions import IsAuthenticated
from course.models import Course, CourseInstanceStudent, CourseInstance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from institute.models import InstituteConfig
import datetime


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
    filterset_fields = ["fnid", "institute_fnid", "student_fnid", "course_instance_fnid"]


    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = CourseInstanceStudent.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")


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
    filterset_fields = ["fnid", "institute_fnid", "course_fnid", "term_fnid"]


    def perform_create(self, serializer):
        start = serializer.validated_data.get("start", False)
        if not start:
            institute_fnid = self.request.query_params.get("institute_fnid", None)
            if institute_fnid:
                #d = get_start_date_from_week(institute_fnid)
                #print("Hello World")
                return serializer.save()#start=d.date())

        return serializer.save()

    def get_queryset(self):
        print("Hello Rob")
        queryset = CourseInstance.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")

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