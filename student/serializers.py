from rest_framework.serializers import ModelSerializer
from student.models import Student
from institute.models import Institute, InstituteDomain
from rest_framework import serializers


class StudentSerializer(ModelSerializer):

    def validate(self, data):
        institute_fnid = data["institute_fnid"]
        email = data["email"]
        domain = email.split("@")[1]

        # Raise error if institute doesn't exist
        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("The institute does not exist.")

        try:
            InstituteDomain.objects.get(institute_fnid=institute_fnid, domain=domain)
        except:
            raise serializers.ValidationError("Student cannot be registered using email domain.")
        return data

    class Meta:
        model = Student
        fields = ('fnid',
                  'institute_fnid',
                  'school_fnid',
                  'programme_fnid',
                  'student_id',
                  'first_name',
                  'last_name',
                  'email',
                  'year_of_study',
                  'international',
                  'verified')

        read_only_fields = ['fnid']