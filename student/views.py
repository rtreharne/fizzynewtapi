from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from student.serializers import StudentSerializer, StudentEmailSerializer
from rest_framework.permissions import IsAuthenticated
from student.models import Student, StudentEmail


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

class ListCreateStudentEmailAPIView(ListCreateAPIView):
    serializer_class = StudentEmailSerializer
    permission_classes = (IsAuthenticated,)

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
        return StudentEmail.objects.all()

class StudentEmailDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentEmailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return StudentEmail.objects.all()