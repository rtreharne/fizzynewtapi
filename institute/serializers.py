from rest_framework.serializers import ModelSerializer
from institute.models import Institute, InstituteDomain
from rest_framework import serializers

class InstituteSerializer(ModelSerializer):
    class Meta:
        model = Institute
        fields = ('fnid', 'name',)

        read_only_fields = ['fnid']

class InstituteDomainSerializer(ModelSerializer):
    class Meta:
        model = InstituteDomain
        fields = ('institute_fnid', 'domain', 'primary')


