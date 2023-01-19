from attendance.views import ListCreateSessionRequestAPIView, \
    ListCreateSessionAPIView, SessionRequestDetailAPIView, \
    SessionDetailAPIView, AttendanceDetailAPIView, ListCreateAttendanceAPIView, \
    ActiveSessionRequestStudent, ActiveSessionRequestCourseInstance

from django.urls import path

urlpatterns = [

    path('request/', ListCreateSessionRequestAPIView.as_view(), name='session-request'),
    path('request/<str:fnid>/', SessionRequestDetailAPIView.as_view(), name='update-session-request'),
    path('session/', ListCreateSessionAPIView.as_view(), name='session-request'),
    path('session/<str:fnid>/', SessionDetailAPIView.as_view(), name='update-session'),
    path('', ListCreateAttendanceAPIView.as_view(), name='attendance'),
    path('session/active-session-requests-student/institute/<str:institute_fnid>/student/<str:student_fnid>/',
         ActiveSessionRequestStudent.as_view(), name="active-session-requests-student"),
    path('session/active-session-requests-course-instance/institute/<str:institute_fnid>/course_instance/<str:course_instance_fnid>/',
             ActiveSessionRequestCourseInstance.as_view(), name="active-session-requests-course-instance"),
    path('<str:fnid>/', AttendanceDetailAPIView.as_view(), name='update-attendance')

]