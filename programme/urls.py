from programme.views import ListCreateProgrammeAPIView, ProgrammeDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateProgrammeAPIView.as_view(), name='create-programme'),
    path('<str:fnid>/', ProgrammeDetailAPIView.as_view(), name="update-programme"),

]