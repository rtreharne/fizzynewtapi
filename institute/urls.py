from institute.views import ListCreateInstituteAPIView, \
    InstituteDetailAPIView, \
    ListCreateInstituteDomainAPIView, \
    InstituteDomainDetailAPIView, ListCreateInstituteConfigAPIView, InstituteConfigDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateInstituteAPIView.as_view(), name='create-institute'),
    path('domain', ListCreateInstituteDomainAPIView.as_view(), name="create-institute-domain"),
    path('config', ListCreateInstituteConfigAPIView.as_view(), name="create-institute-config"),
    path('<str:fnid>', InstituteDetailAPIView.as_view(), name="update-institute"),
    path('domain/<str:fnid>', InstituteDomainDetailAPIView.as_view(), name="update-institute-domain"),
    path('config/<str:fnid>', InstituteConfigDetailAPIView.as_view(), name="update-institute-config")
]