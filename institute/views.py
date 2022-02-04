from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from institute.serializers import InstituteSerializer, InstituteEmailSerializer
from rest_framework.permissions import IsAuthenticated
from institute.models import Institute, InstituteDomain
from django.core.exceptions import ObjectDoesNotExist



class CreateInstituteAPIView(CreateAPIView):
    serializer_class = InstituteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

class InstituteDomainListAPIView(ListCreateAPIView):
    serializer_class = InstituteEmailSerializer
    queryset = InstituteDomain.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        institute_fnid = self.request.data["institute_fnid"]

        try:
            Institute.objects.get(fnid=institute_fnid)
            if serializer["primary"]:
                [x.update(primary=False) for x in InstituteDomain.objects.filter(institute_fnid=institute_fnid)]
        except:
            return Response({'error': 'Institute does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return self.queryset.all()

class InstituteListAPIView(ListAPIView):
    serializer_class=InstituteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Institute.objects.all()

class InstituteDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InstituteSerializer
    queryset = Institute.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self, *args, **kwargs):
        print(self.kwargs["fnid"])
        return Institute.objects.get(fnid=self.kwargs["fnid"])

