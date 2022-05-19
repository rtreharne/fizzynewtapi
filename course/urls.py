from course.views import ListCreateCourseAPIView, \
    CourseDetailAPIView, \
    ListCreateCourseStudentAPIView, \
    CourseStudentDetailAPIView, \
    ListCreateCourseInstanceAPIView, \
    CourseInstanceDetailAPIView


from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [

    path('', ListCreateCourseAPIView.as_view(), name='create-course'),
    path('instance/', ListCreateCourseInstanceAPIView.as_view(), name="create-course-instance"),
    path('student/', ListCreateCourseStudentAPIView.as_view(), name='create-course-student'),
    path('<str:fnid>/', CourseDetailAPIView.as_view(), name="update-course"),
    path('student/<str:fnid>/', CourseStudentDetailAPIView.as_view(), name="update-course-student"),
    path('instance/<str:fnid>/', CourseInstanceDetailAPIView.as_view(), name="update-course-instance"),


]