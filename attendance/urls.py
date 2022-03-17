from attendance.views import ListCreateCodeAPIView, ListCreateSessionTypeAPIView, ListCreateAttendanceAPIView
from django.urls import path
from rest_framework import routers

#router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [

    path('', ListCreateAttendanceAPIView.as_view(), name='create-attendance'),
    path('code/', ListCreateCodeAPIView.as_view(), name='create-code'),
    path('session/type/', ListCreateSessionTypeAPIView.as_view(), name='create-session-type')

]