from school.views import ListCreateSchoolAPIView, SchoolDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateSchoolAPIView.as_view(), name='list-create-school'),
    path('<str:fnid>', SchoolDetailAPIView.as_view(), name="update-school"),


]