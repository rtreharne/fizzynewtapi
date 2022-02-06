from rest_framework.serializers import ModelSerializer
from school.models import School
from institute.models import Institute
from rest_framework import serializers


class SchoolSerializer(ModelSerializer):

    def validate(self, data):
        institute_fnid = data["institute_fnid"]
        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("The institute does not exist.")

        return data

    class Meta:
        model = School
        fields = ('fnid', 'institute_fnid', 'name')
        read_only_fields = ['fnid']