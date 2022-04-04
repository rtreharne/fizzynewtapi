from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from course.serializers import CourseSerializer, CourseStudentSerializer
from rest_framework.permissions import IsAuthenticated
from course.models import Course, CourseStudent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions


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


class ListCreateCourseStudentAPIView(ListCreateAPIView):
    serializer_class = CourseStudentSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid", "institute_fnid", "student_fnid", "course_fnid"]


    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = CourseStudent.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")


class CourseStudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseStudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid", "student_fnid"]


    def get_queryset(self):

        queryset = CourseStudent.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnide not supplied in query string.")




