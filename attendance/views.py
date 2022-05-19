from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from attendance.serializers import CodeSerializer, SessionTypeSerializer, AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from attendance.models import Code, SessionType, Attendance, Session
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from attendance_toolkit import toolkit
from django.conf import settings
import pytz
from institute.models import Institute
from datetime import timedelta
from attendance_toolkit.toolkit import get_session_start, check_for_session, create_attendance_log_for_session


class ListCreateCodeAPIView(ListCreateAPIView):
    serializer_class = CodeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = Code.objects.all()
        return queryset

class ListCreateSessionTypeAPIView(ListCreateAPIView):
    serializer_class = SessionTypeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = SessionType.objects.all()
        return queryset

class ListCreateAttendanceAPIView(ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid", "course_fnid", "student_fnid"]

    def perform_create(self, serializer):

        serializer.is_valid()

        session = check_for_session(serializer.validated_data, self.request.query_params)

        return serializer

    def get_queryset(self):
        queryset = Attendance.objects.all()
        return queryset
        institute_fnid = self.request.query_params.get("institute_fnid", None)

        if institute_fnid:
            return Institute.objects.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")



