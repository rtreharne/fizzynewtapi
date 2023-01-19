from attendance.views import ListCreateSessionRequestAPIView, \
    ListCreateSessionAPIView, SessionRequestDetailAPIView, \
    SessionDetailAPIView, AttendanceDetailAPIView, ListCreateAttendanceAPIView, \
    ActiveSessionRequestStudent, ActiveSessionRequestCourseInstance, \
    ActiveSessionCourseInstance, ActiveSessionStudent, \
    AttendanceBySession, AttendanceBySessionByStudent

from django.urls import path

urlpatterns = [

    path('request/', ListCreateSessionRequestAPIView.as_view(), name='session-request'),
    path('request/<str:fnid>/', SessionRequestDetailAPIView.as_view(), name='update-session-request'),
    path('session/', ListCreateSessionAPIView.as_view(), name='session-request'),
    path('session/<str:fnid>/', SessionDetailAPIView.as_view(), name='update-session'),
    path('', ListCreateAttendanceAPIView.as_view(), name='attendance'),
    path('attendance-by-session/institute/<str:institute_fnid>/session/<str:session_fnid>/',
         AttendanceBySession.as_view(), name="attendance-by-session"),
    path('attendance-by-session-by-student/institute/<str:institute_fnid>/session/<str:session_fnid>/student/<str:student_fnid>/',
             AttendanceBySessionByStudent.as_view(), name="attendance-by-session-by-student"),
    path('session/active-session-requests-student/institute/<str:institute_fnid>/student/<str:student_fnid>/',
         ActiveSessionRequestStudent.as_view(), name="active-session-requests-student"),
    path('session/active-session-student/institute/<str:institute_fnid>/student/<str:student_fnid>/',
         ActiveSessionStudent.as_view(), name="active-session-student"),

    path('session/active-session-requests-course-instance/institute/<str:institute_fnid>/course_instance/<str:course_instance_fnid>/',
             ActiveSessionRequestCourseInstance.as_view(), name="active-session-requests-course-instance"),
    path('session/active-session-course-instance/institute/<str:institute_fnid>/course_instance/<str:course_instance_fnid>/',
        ActiveSessionCourseInstance.as_view(), name="active-session-course-instance"),
    path('<str:fnid>/', AttendanceDetailAPIView.as_view(), name='update-attendance')

]