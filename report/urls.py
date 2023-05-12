from django.urls import path
from rest_framework import routers
from .views import ActiveSession

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('livesessionoverview/', ActiveSession.as_view(), name="active-sessions")
]