from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from attendance.models import Code, SessionType, Attendance, Session
from institute.models import Institute

class CodeSerializer(ModelSerializer):

    class Meta:
        model = Code
        fields = ('fnid', 'code')
        read_only_fields = ['fnid']

class SessionSerializer(ModelSerializer):

    class Meta:
        model = Session
        fields = ('fnid', 'code')
        read_only_fields = ['fnid']

class SessionTypeSerializer(ModelSerializer):
    class Meta:
        model = SessionType
        fields = ('fnid', 'name')
        read_only_fields = ['fnid']

class AttendanceSerializer(ModelSerializer):

    def validate(self, data):
        institute_fnid = data["institute_fnid"]
        # Raise error if institute doesn't exist
        try:
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("This institute does not exist")

        return data

    class Meta:
        model = Attendance
        fields = ('fnid',
                  'institute_fnid',
                  'school_fnid',
                  'course_fnid',
                  'student_fnid',
                  'session_type_fnid',
                  'group_fnid',
                  'session_code',
                  'online')

        read_only_fields = ['fnid', 'created_at']