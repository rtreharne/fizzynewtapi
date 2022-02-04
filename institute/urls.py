from institute.views import CreateInstituteAPIView, InstituteListAPIView, InstituteDetailAPIView, CreateInstituteDomainListAPIView, InstituteDomainListAPIView
from django.urls import path

urlpatterns = [

    path('create', CreateInstituteAPIView.as_view(), name='create-institute'),
    path('domain/create', CreateInstituteDomainListAPIView.as_view(), name="create-institute-domain"),
    path('domain', InstituteDomainListAPIView.as_view(), name="list-domain-institute"),
    path('', InstituteListAPIView.as_view(), name="list-institute"),
    path('<str:fnid>', InstituteDetailAPIView.as_view(), name="update-institute"),
]