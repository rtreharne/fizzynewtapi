from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from school.serializers import SchoolSerializer
from rest_framework.permissions import IsAuthenticated
from school.models import School
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from school.models import School
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from helpers.token_params import *

class ListCreateSchoolAPIView(ListCreateAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid", "institute_fnid", "name"]

    def perform_create(self, serializer):
        serializer.is_valid()
        return serializer.save()

    def get_queryset(self):
        queryset = School.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SchoolDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = School.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

