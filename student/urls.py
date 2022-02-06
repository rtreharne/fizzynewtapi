from student.views import ListCreateStudentAPIView, StudentDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateStudentAPIView.as_view(), name='list-create-student'),
    path('<str:fnid>', StudentDetailAPIView.as_view(), name="student-school"),

]