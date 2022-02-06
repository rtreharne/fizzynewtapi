from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from programme.serializers import ProgrammeSerializer
from rest_framework.permissions import IsAuthenticated
from programme.models import Programme


class ListCreateProgrammeAPIView(ListCreateAPIView):
    serializer_class = ProgrammeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return Programme.objects.all()

class ProgrammeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProgrammeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return Programme.objects.all()

