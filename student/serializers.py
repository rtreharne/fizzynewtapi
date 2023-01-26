from rest_framework.serializers import ModelSerializer
from student.models import Student, StudentEmail, StudentTerm
from institute.models import Institute, InstituteDomain
from rest_framework import serializers


class StudentSerializer(ModelSerializer):

    def validate(self, data):
        institute_fnid = data["institute_fnid"]

        # Raise error if institute doesn't exist
        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("The institute does not exist.")

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
                  'undergraduate',
                  'year_of_study',
                  'international',
                  'verified',
                  'average_attend_pc')

        read_only_fields = ['fnid']

class StudentEmailSerializer(ModelSerializer):

    def validate(self, data):
        institute_fnid = data["institute_fnid"]
        email = data["email"]
        domain = email.split("@")[1]
        student_fnid = data["student_fnid"]
        # Raise error if institute doesn't exist
        try:
            Student.objects.get(fnid=student_fnid)
        except:
            raise serializers.ValidationError("This student does not exist")

        try:
            InstituteDomain.objects.get(institute_fnid=institute_fnid, domain=domain)
        except:
            raise serializers.ValidationError("Student cannot be registered using email domain.")

        return data

    class Meta:
        model = StudentEmail
        fields = ('fnid', 'institute_fnid', 'student_fnid', 'email', 'primary')

        read_only_fields = ['fnid']

class StudentTermSerializer(ModelSerializer):

    def validate(self, data):
        institute_fnid = data["institute_fnid"]
        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("The institute does not exist.")

        return data

    class Meta:
        model = StudentTerm
        fields = ('fnid', 'institute_fnid', 'student_fnid', 'term_fnid', 'current')
        read_only_fields = ['fnid']