from institute.views import CreateInstituteAPIView, InstituteListAPIView
from django.urls import path

urlpatterns = [
    path('create', CreateInstituteAPIView.as_view(), name='create-institute'),
    path('', InstituteListAPIView.as_view(), name="list-institute")
]