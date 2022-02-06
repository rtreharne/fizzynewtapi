from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from institute.serializers import InstituteSerializer, InstituteDomainSerializer
from rest_framework.permissions import IsAuthenticated
from institute.models import Institute, InstituteDomain
from django.core.exceptions import ObjectDoesNotExist



class ListCreateInstituteAPIView(ListCreateAPIView):
    serializer_class = InstituteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return Institute.objects.all()


class ListCreateInstituteDomainAPIView(ListCreateAPIView):
    serializer_class = InstituteDomainSerializer
    queryset = InstituteDomain.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.is_valid()

        # Set primary field to False for all existing institute domains if new domain is primary
        existing_domains = InstituteDomain.objects.filter(institute_fnid=serializer.validated_data["institute_fnid"])
        if serializer.validated_data.get("primary", False):

            if len(existing_domains) > 0:
                existing_domains.update(primary=False)

        elif len(existing_domains) == 0:
            return serializer.save(primary=True)

        return serializer.save()

    def get_queryset(self):
        return InstituteDomain.objects.all()


class InstituteDomainDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InstituteDomainSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):
        return InstituteDomain.objects.all()



class InstituteDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InstituteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return Institute.objects.all()

