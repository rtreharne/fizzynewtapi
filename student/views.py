from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from student.serializers import StudentSerializer, StudentEmailSerializer
from rest_framework.permissions import IsAuthenticated
from student.models import Student, StudentEmail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions


class ListCreateStudentAPIView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["fnid", "institute_fnid", "last_name", "first_name", "school_fnid"]



    def perform_create(self, serializer):
        serializer.is_valid()
        return serializer.save()

    def get_queryset(self):
        queryset = Student.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")



class StudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = Student.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset

class ListCreateStudentEmailAPIView(ListCreateAPIView):
    serializer_class = StudentEmailSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["fnid", "institute_fnid", "student_fnid", "primary", "email"]

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
        queryset = StudentEmail.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")


class StudentEmailDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentEmailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = StudentEmail.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")