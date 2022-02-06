from rest_framework.serializers import ModelSerializer
from programme.models import Programme
from institute.models import Institute
from school.models import School
from rest_framework import serializers

class ProgrammeSerializer(ModelSerializer):

    def validate(self, data):
        institute_fnid = data["institute_fnid"]
        school_fnid = data["school_fnid"]

        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("The institute does not exist.")

        try:
            School.objects.get(fnid=school_fnid)
        except:
            raise serializers.ValidationError("The school does not exist.")

        return data

    class Meta:
        model = Programme
        fields = ('fnid', 'institute_fnid', 'school_fnid', 'name')
        read_only_fields = ['fnid']