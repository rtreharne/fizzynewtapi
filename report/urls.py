from report.views import StudentFullReport, StudentSummaryReport
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [

    path('summary/', StudentSummaryReport.as_view(), name='summary'),

]