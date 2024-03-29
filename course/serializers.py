from rest_framework.serializers import ModelSerializer
from course.models import Course, CourseInstanceStudent, CourseInstance, Group, GroupStudent
from institute.models import Institute
from rest_framework import serializers

class CourseSerializer(ModelSerializer):
    def validate(self, data):
        print(data)

        # Raise error if institute doesn't exist
        try:
            institute_fnid = data["institute_fnid"]
            Institute.objects.get(fnid=institute_fnid)
        except:
            raise serializers.ValidationError("The institute does not exist.")

        return data

    class Meta:
        model = Course
        fields = ('fnid', 'institute_fnid', 'code', 'name', 'visible')
        read_only_fields = ['fnid']


class CourseInstanceStudentSerializer(ModelSerializer):

    class Meta:
        model = CourseInstanceStudent
        fields = ('fnid', 'institute_fnid', 'student_fnid', 'course_instance_fnid', 'average_attend_pc', 'resit')
        read_only_fields = ['fnid']


class CourseInstanceSerializer(ModelSerializer):

    class Meta:
        model = CourseInstance
        fields = ('fnid', 'institute_fnid', 'course_fnid', 'term_fnid', 'name_override', 'start_date_override', 'end_date_override')
        read_only_fields = ['fnid']

class GroupSerializer(ModelSerializer):
    
    class Meta:
        model = Group
        fields = ('fnid', 'institute_fnid', 'course_instance_fnid', 'name')
        read_only_fields = ['fnid']

class GroupStudentSerializer(ModelSerializer):
        
    class Meta:
        model = GroupStudent
        fields = ('fnid', 'institute_fnid', 'group_fnid', 'student_fnid')
        read_only_fields = ['fnid']