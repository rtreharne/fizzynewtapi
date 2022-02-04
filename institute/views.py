from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from institute.serializers import InstituteSerializer, InstituteDomainSerializer
from rest_framework.permissions import IsAuthenticated
from institute.models import Institute, InstituteDomain
from django.core.exceptions import ObjectDoesNotExist



class CreateInstituteAPIView(CreateAPIView):
    serializer_class = InstituteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()


class CreateInstituteDomainListAPIView(CreateAPIView):
    serializer_class = InstituteDomainSerializer
    queryset = InstituteDomain.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        print(serializer)
        return serializer.save()

    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            institute_fnid = self.request.data["institute_fnid"]
        except KeyError:
            return Response({'error': 'institute_fnid required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Institute.objects.get(fnid=institute_fnid)
            if serializer["primary"]:
                [x.update(primary=False) for x in InstituteDomain.objects.filter(institute_fnid=institute_fnid)]
        except ObjectDoesNotExist:
            return Response({'error': 'Institute does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        #self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    """

class InstituteDomainListAPIView(ListAPIView):
    serializer_class=InstituteDomainSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return InstituteDomain.objects.all()


class InstituteListAPIView(ListAPIView):
    serializer_class=InstituteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Institute.objects.all()

class InstituteDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InstituteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return Institute.objects.all()

