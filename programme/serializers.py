from rest_framework.serializers import ModelSerializer
from programme.models import Programme
from institute.models import Institute
from school.models import School
from rest_framework import serializers

class ProgrammeSerializer(ModelSerializer):

    def validate(self, data):

        try:
            institute_fnid = data["institute_fnid"]
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("The institute does not exist.")

        try:
            school_fnid = data["school_fnid"]
            School.objects.get(fnid=school_fnid, institute_fnid=institute_fnid)
        except:
            raise serializers.ValidationError("The school for this programme does not exist at this institute.")

        return data

    class Meta:
        model = Programme
        fields = ('fnid', 'institute_fnid', 'school_fnid', 'name')
        read_only_fields = ['fnid']