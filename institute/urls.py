from institute.views import ListCreateInstituteAPIView, \
    InstituteDetailAPIView, \
    ListCreateInstituteDomainAPIView, \
    InstituteDomainDetailAPIView, ListCreateInstituteConfigAPIView, InstituteConfigDetailAPIView, \
    TermDetailAPIView, ListCreateTermAPIView, ListCreateYearAPIView, YearDetailAPIView, ListCreateSessionTypeAPIView, SessionTypeDetailAPIView
from django.urls import path

urlpatterns = [

    path('', ListCreateInstituteAPIView.as_view(), name='create-institute'),
    path('domain/', ListCreateInstituteDomainAPIView.as_view(), name="create-institute-domain"),
    path('config/', ListCreateInstituteConfigAPIView.as_view(), name="create-institute-config"),
    path('term/', ListCreateTermAPIView.as_view(), name='term-create'),
    path('year/', ListCreateYearAPIView.as_view(), name='year-create'),
    path('sessiontype/', ListCreateSessionTypeAPIView.as_view(), name='session-type-create'),
    path('<str:fnid>/', InstituteDetailAPIView.as_view(), name="update-institute"),
    path('domain/<str:fnid>/', InstituteDomainDetailAPIView.as_view(), name="update-institute-domain"),
    path('config/<str:fnid>/', InstituteConfigDetailAPIView.as_view(), name="update-institute-config"),
    path('term/<str:fnid>/', TermDetailAPIView.as_view(), name="term"),
    path('year/<str:fnid>/', YearDetailAPIView.as_view(), name="year"),
    path('sessiontype/<str:fnid>/', SessionTypeDetailAPIView.as_view(), name="sessiontype")
]