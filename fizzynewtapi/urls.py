"""fizzynewtapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from report.views import ActiveSession, AttendanceOverview, CountActiveStudents, ConsecutiveAbsence, AttendanceThreshold, SchoolCount, CourseInstanceCount, ProgrammeCount

schema_view = get_schema_view(
   openapi.Info(
      title="Fizzy Newt API",
      default_version='v1',
      description="Documentation for Fizzy Newt API",
      #terms_of_service="",
      #contact=openapi.Contact(email="contact@snippets.local"),
      #license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
    authentication_classes=[]
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/auth/', include("authentication.urls")),
    path('api/institute/', include("institute.urls")),
    path('api/school/', include("school.urls")),
    path('api/programme/', include("programme.urls")),
    path('api/course/', include("course.urls")),
    path('api/student/', include("student.urls")),
    path('api/attendance/', include("attendance.urls")),
    path('api/report/', include("report.urls")),
    path('api/livesessionoverview/', ActiveSession.as_view(), name="live-session-overview"),
    path('api/attendancebandoverview/', AttendanceOverview.as_view(), name="attendance-overview"),
    path('api/activestudents/', CountActiveStudents.as_view(), name="active-students"),
    path('api/consecutiveabsence/', ConsecutiveAbsence.as_view(), name="consecutive-absence"),
    path('api/attendancethreshold/', AttendanceThreshold.as_view(), name="attendance-threshold"),
    path('api/schoolcount/', SchoolCount.as_view(), name="school-count"),
    path('api/courseinstancecount/', CourseInstanceCount.as_view(), name="course-instance-count"),
    path('api/programmecount/', ProgrammeCount.as_view(), name="programme-count"),


    #path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
