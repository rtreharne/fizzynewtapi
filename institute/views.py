from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from institute.serializers import InstituteSerializer, InstituteDomainSerializer, InstituteConfigSerializer, TermSerializer, YearSerializer, SessionTypeSerializer
from rest_framework.permissions import IsAuthenticated
from institute.models import Institute, InstituteDomain, InstituteConfig, Term, Year, SessionType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from django_filters.rest_framework import DjangoFilterBackend



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
        return queryset


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
        return InstituteConfig.objects.all()


class InstituteConfigDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InstituteConfigSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return InstituteConfig.objects.all()

class ListCreateTermAPIView(ListCreateAPIView):
    serializer_class = TermSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid", "institute_fnid", "label", "start_date", "end_date"]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = Term.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

class TermDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TermSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = Term.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset

class ListCreateYearAPIView(ListCreateAPIView):
    serializer_class = YearSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid", "institute_fnid", "label"]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = Year.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

class YearDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = YearSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = Year.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset

class ListCreateSessionTypeAPIView(ListCreateAPIView):
    serializer_class = SessionTypeSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid", "institute_fnid", "label"]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        queryset = SessionType.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")

class SessionTypeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionTypeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    lookup_field = "fnid"

    filterset_fields = ["institute_fnid"]

    def get_queryset(self):

        queryset = SessionType.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_id not supplied in query string.")
        return queryset