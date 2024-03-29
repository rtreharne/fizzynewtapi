from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from attendance.models import SessionRequest, Session, Attendance

class SessionRequestSerializer(ModelSerializer):

    class Meta:
        model = SessionRequest
        fields = ('fnid',
                  'institute_fnid',
                  'course_instance_fnid',
                  'session_type_fnid',
                  'student_fnid',
                  'group_fnid',
                  'session_start',
                  'duration_mins',
                  'session_fnid',
                  'expired',
                  )

        read_only_fields = ['fnid']


class SessionSerializer(ModelSerializer):

    class Meta:
        model = Session
        fields = ('fnid',
                  'institute_fnid',
                  'course_instance_fnid',
                  'session_type_fnid',
                  'group_fnid',
                  'session_start',
                  'duration_mins',
                  'expired',
                  'online',
                  'cancelled_by',
                  'cancelled',
                  'mandatory',
                  'void',)

        read_only_fields = ['fnid']


class AttendanceSerializer(ModelSerializer):
    lookup_field = 'fnid'
    class Meta:
        model= Attendance
        fields = (
            'fnid',
            'institute_fnid',
            'school_fnid',
            'programme_fnid',
            'course_instance_fnid',
            'session_fnid',
            'student_fnid',
            'session_type_fnid',
            'group_fnid',
            'present',
            'verified',
            'late',
            'void',
            'verified_by_administrator',
            'verified_by_audit',
            'approved_absence',
                  )

        read_only_fields = ['fnid']

