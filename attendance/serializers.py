from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from attendance.models import SessionRequest, Session

class SessionRequestSerializer(ModelSerializer):

    class Meta:
        model = SessionRequest
        fields = ('fnid',
                  'institute_fnid',
                  'course_instance_fnid',
                  'session_type_fnid',
                  'student_fnid',
                  'session_start',
                  'duration_hrs'
                  )

        read_only_fields = ['fnid']

class SessionSerializer(ModelSerializer):

    class Meta:
        model = Session
        fields = ('fnid',
                  'institute_fnid',
                  'course_instance_fnid',
                  'session_type_fnid',
                  'session_start',
                  'duration_hrs')

        read_only_fields = ['fnid']


