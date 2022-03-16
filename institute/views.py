from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from institute.serializers import InstituteSerializer, InstituteDomainSerializer, InstituteConfigSerializer
from rest_framework.permissions import IsAuthenticated
from institute.models import Institute, InstituteDomain, InstituteConfig
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions



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
        queryset = InstituteDomain.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")


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


class ListCreateInstituteConfigAPIView(ListCreateAPIView):
    serializer_class = InstituteConfigSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return Institute.objects.all()


class InstituteConfigDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InstituteConfigSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return Institute.objects.all()