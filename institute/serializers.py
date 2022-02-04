from rest_framework.serializers import ModelSerializer
from institute.models import Institute, InstituteDomain

class InstituteSerializer(ModelSerializer):
    class Meta:
        model = Institute
        fields = ('fnid', 'name',)

        read_only_fields = ['fnid']

class InstituteEmailSerializer(ModelSerializer):
    class Meta:
        model = InstituteDomain
        fields = ('institute_fnid', 'domain', 'primary')


