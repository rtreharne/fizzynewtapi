from rest_framework.serializers import ModelSerializer
from institute.models import Institute, InstituteDomain
from rest_framework import serializers
from institute.models import Institute

class InstituteSerializer(ModelSerializer):


    class Meta:
        model = Institute
        fields = ('fnid', 'name',)

        read_only_fields = ['fnid']

class InstituteDomainSerializer(ModelSerializer):


    def validate(self, data):
        print("validating data")
        institute_fnid = data["institute_fnid"]
        # Raise error if institute doesn't exist
        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("This institute does not exist")

        return data


    class Meta:
        model = InstituteDomain
        fields = ('institute_fnid', 'domain', 'primary')


