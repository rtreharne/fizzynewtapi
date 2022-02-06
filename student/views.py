from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from student.serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from student.models import Student


class ListCreateStudentAPIView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.is_valid()
        return serializer.save()

    def get_queryset(self):
        return Student.objects.all()


class StudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return Student.objects.all()

