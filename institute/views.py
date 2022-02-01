from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from institute.serializers import InstituteSerializer
from rest_framework.permissions import IsAuthenticated
from institute.models import Institute



class CreateInstituteAPIView(CreateAPIView):
    serializer_class = InstituteSerializer
    permission_classes = (IsAuthenticated,)

    print("hello rob")

    def perform_create(self, serializer):
        return serializer.save()

class InstituteListAPIView(ListAPIView):
    serializer_class=InstituteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Institute.objects.all()


