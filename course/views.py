from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from course.serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated
from course.models import Course


class ListCreateCourseAPIView(ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return Course.objects.all()


class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return Course.objects.all()

