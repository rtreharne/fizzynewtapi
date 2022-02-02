from institute.views import CreateInstituteAPIView, InstituteListAPIView, InstituteDetailAPIView
from django.urls import path

urlpatterns = [
    path('create', CreateInstituteAPIView.as_view(), name='create-institute'),
    path('', InstituteListAPIView.as_view(), name="list-institute"),
    path('<str:fnid>', InstituteDetailAPIView.as_view(), name="update-institute")
]