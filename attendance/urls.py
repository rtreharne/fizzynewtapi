from attendance.views import ListCreateSessionRequestAPIView, \
    ListCreateSessionAPIView, SessionRequestDetailAPIView, \
    SessionDetailAPIView, AttendanceDetailAPIView, ListCreateAttendanceAPIView, AverageAttendance, UpdateAverageAttendance

from report.views import ActiveSession

from django.urls import path

urlpatterns = [

    path('request/', ListCreateSessionRequestAPIView.as_view(), name='session-request'),
    path('session/', ListCreateSessionAPIView.as_view(), name='session-request'),
    path('average/', AverageAttendance.as_view(), name='average-attendance'),
    path('updateaverage/', UpdateAverageAttendance.as_view(), name='update-average-attendance'),
    path('', ListCreateAttendanceAPIView.as_view(), name="create-attendance"),
    path('request/<str:fnid>/', SessionRequestDetailAPIView.as_view(), name='update-session-request'),
    path('session/<str:fnid>/', SessionDetailAPIView.as_view(), name='update-session'),
    path('<str:fnid>/', AttendanceDetailAPIView.as_view(), name='update-attendance'),



]