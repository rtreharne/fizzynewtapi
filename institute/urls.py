from institute.views import CreateInstituteAPIView, InstituteListAPIView, InstituteDetailAPIView, InstituteDomainListAPIView
from django.urls import path

urlpatterns = [
    path('<str:fnid>', InstituteDetailAPIView.as_view(), name="update-institute"),
    path('create', CreateInstituteAPIView.as_view(), name='create-institute'),
    path('', InstituteListAPIView.as_view(), name="list-institute"),
    path('domain', InstituteDomainListAPIView.as_view(), name="institute-domain")
]