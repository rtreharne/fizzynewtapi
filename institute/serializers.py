from rest_framework.serializers import ModelSerializer
from institute.models import Institute, InstituteDomain, InstituteConfig
from rest_framework import serializers

class InstituteSerializer(ModelSerializer):

    class Meta:
        model = Institute
        fields = ('fnid', 'name',)

        read_only_fields = ['fnid']

class InstituteDomainSerializer(ModelSerializer):


    def validate(self, data):
        institute_fnid = data["institute_fnid"]
        # Raise error if institute doesn't exist
        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("This institute does not exist")

        return data


    class Meta:
        model = InstituteDomain
        fields = ('fnid', 'institute_fnid', 'domain', 'primary')

        read_only_fields = ['fnid']


class InstituteConfigSerializer(ModelSerializer):

    class Meta:
        model = InstituteConfig
        fields = ('fnid', 'institute_fnid', 'student_id_required')

        read_only_fields = ['fnid']