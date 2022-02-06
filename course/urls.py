from course.views import ListCreateCourseAPIView, CourseDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateCourseAPIView.as_view(), name='create-programme'),
    #path('', CourseListAPIView.as_view(), name="list-programme"),
    path('<str:fnid>', CourseDetailAPIView.as_view(), name="update-programme"),

]