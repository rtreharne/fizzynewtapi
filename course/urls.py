from course.views import ListCreateCourseAPIView, \
    CourseDetailAPIView, \
    ListCreateCourseInstanceStudentAPIView, \
    CourseStudentDetailAPIView, \
    ListCreateCourseInstanceAPIView, \
    CourseInstanceDetailAPIView


from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [

    path('', ListCreateCourseAPIView.as_view(), name='create-course'),
    path('instance/', ListCreateCourseInstanceAPIView.as_view(), name="create-course-instance"),
    path('instance/student/', ListCreateCourseInstanceStudentAPIView.as_view(), name='create-course-student'),
    path('<str:fnid>/', CourseDetailAPIView.as_view(), name="update-course"),
    path('instance/student/<str:fnid>/', CourseStudentDetailAPIView.as_view(), name="update-course-student"),
    path('instance/<str:fnid>/', CourseInstanceDetailAPIView.as_view(), name="update-course-instance"),


]