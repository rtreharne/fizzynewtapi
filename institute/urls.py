from institute.views import ListCreateInstituteAPIView, \
    InstituteDetailAPIView, \
    ListCreateInstituteDomainAPIView, \
    InstituteDomainDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateInstituteAPIView.as_view(), name='create-institute'),
    path('domain', ListCreateInstituteDomainAPIView.as_view(), name="create-institute-domain"),
    path('<str:fnid>', InstituteDetailAPIView.as_view(), name="update-institute"),
    path('domain/<str:fnid>', InstituteDomainDetailAPIView.as_view(), name="update-institute-domain")
]