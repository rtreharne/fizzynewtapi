from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from school.serializers import SchoolSerializer
from rest_framework.permissions import IsAuthenticated
from school.models import School


class ListCreateSchoolAPIView(ListCreateAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.is_valid()
        return serializer.save()

    def get_queryset(self):
        return School.objects.all()


class SchoolDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "fnid"

    def get_queryset(self):

        return School.objects.all()

