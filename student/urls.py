from student.views import ListCreateStudentAPIView, StudentDetailAPIView, ListCreateStudentEmailAPIView, StudentEmailDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateStudentAPIView.as_view(), name='list-create-student'),
    path('email/', ListCreateStudentEmailAPIView.as_view(), name='list-create-student-email'),
    path('email/<str:fnid>/', StudentEmailDetailAPIView.as_view(), name="student-email"),
    path('<str:fnid>/', StudentDetailAPIView.as_view(), name="student"),
    path('email/<str:fnid>/', StudentEmailDetailAPIView.as_view(), name="student-email"),

]