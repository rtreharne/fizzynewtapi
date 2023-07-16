from django.urls import path
from rest_framework import routers
from .views import ActiveSession, AttendanceOverview, ConsecutiveAbsence, AttendanceThreshold

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('livesessionoverview/', ActiveSession.as_view(), name="active-sessions"),
    path('attendancebandoverview/', AttendanceOverview.as_view(), name="attendance-overview"),
    path('consecutiveabsence/', ConsecutiveAbsence.as_view(), name="consecutive-absence"),
    path('attendancethreshold/', AttendanceThreshold.as_view(), name="attendance-threshold"),
]