from django.urls import path
from rest_framework import routers
from .views import ActiveSessionRequest

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    #path('active-session-requests-student/institute/<str:institute_fnid>/student/<str:student_fnid>/', ActiveSessionRequest.as_view(), name="active-session-requests-student")
]