from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
#from attendance.serializers import SessionTypeSerializer, AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from attendance.models import SessionType, Attendance, Session
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions

from django.conf import settings
import pytz
from institute.models import Institute
from datetime import timedelta







