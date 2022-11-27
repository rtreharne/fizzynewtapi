from attendance.views import ListCreateSessionRequestAPIView, \
    ListCreateSessionAPIView, SessionRequestDetailAPIView, \
    SessionDetailAPIView, AttendanceDetailAPIView, ListCreateAttendanceAPIView

from django.urls import path

urlpatterns = [

    path('request/', ListCreateSessionRequestAPIView.as_view(), name='session-request'),
    path('request/<str:fnid>/', SessionRequestDetailAPIView.as_view(), name='create-session-request'),
    path('session/', ListCreateSessionAPIView.as_view(), name='session-request'),
    path('session/<str:fnid>/', SessionRequestDetailAPIView.as_view(), name='create-session-request'),
    path('', ListCreateAttendanceAPIView.as_view(), name='attendance'),
    path('<str:fnid>/', AttendanceDetailAPIView.as_view(), name='update-attendance')

]