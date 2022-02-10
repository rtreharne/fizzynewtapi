from course.views import ListCreateCourseAPIView, CourseDetailAPIView, ListCreateCourseStudentAPIView, CourseStudentDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateCourseAPIView.as_view(), name='create-course'),
    path('student/', ListCreateCourseStudentAPIView.as_view(), name='create-course-student'),
    #path('', CourseListAPIView.as_view(), name="list-programme"),
    path('<str:fnid>/', CourseDetailAPIView.as_view(), name="update-course"),
    path('student/<str:fnid>/', CourseStudentDetailAPIView.as_view(), name="update-course-student"),

]