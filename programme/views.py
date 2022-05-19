from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from programme.serializers import ProgrammeSerializer
from rest_framework.permissions import IsAuthenticated
from programme.models import Programme
from institute.models import Institute, InstituteConfig
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions

class ListCreateProgrammeAPIView(ListCreateAPIView):
    serializer_class = ProgrammeSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fnid", "institute_fnid", "name", "school_fnid"]


    def perform_create(self, serializer):
        term_start_week = serializer.validated_data.get("term_start_week", False)
        if not term_start_week:
            institute_fnid = self.request.query_params.get("institute_fnid", None)
            if institute_fnid:
                institute_config = InstituteConfig.objects.get(institute_fnid=institute_fnid)
                serializer.save(term_start_week=institute_config.term_start_week)

        return serializer.save()

    def get_queryset(self):
        queryset = Programme.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            return queryset
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")


class ProgrammeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProgrammeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["institute_fnid"]


    def get_queryset(self):

        queryset = Programme.objects.all()
        institute_fnid = self.request.query_params.get("institute_fnid", None)
        if institute_fnid:
            queryset = queryset.filter(institute_fnid=institute_fnid)
        else:
            raise exceptions.ParseError("institute_fnid not supplied in query string.")
        return queryset

