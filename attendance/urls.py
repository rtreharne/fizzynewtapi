from attendance.views import ListCreateSessionRequestAPIView, \
    ListCreateSessionAPIView, SessionRequestDetailAPIView, \
    SessionDetailAPIView, AttendanceDetailAPIView, ListCreateAttendanceAPIView

from django.urls import path

urlpatterns = [

    path('request/', ListCreateSessionRequestAPIView.as_view(), name='session-request'),
    path('request/<str:fnid>/', SessionRequestDetailAPIView.as_view(), name='update-session-request'),
    path('session/', ListCreateSessionAPIView.as_view(), name='session-request'),
    path('session/<str:fnid>/', SessionDetailAPIView.as_view(), name='update-session'),
    path('', ListCreateAttendanceAPIView.as_view(), name='attendance'),
    path('<str:fnid>/', AttendanceDetailAPIView.as_view(), name='update-attendance')

]