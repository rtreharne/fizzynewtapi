from rest_framework.serializers import ModelSerializer
from course.models import Course, CourseStudent

class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = ('fnid', 'institute_fnid', 'code', 'name', 'visible')
        read_only_fields = ['fnid']

class CourseStudentSerializer(ModelSerializer):

    class Meta:
        model = CourseStudent
        fields = ('fnid', 'course_fnid', 'student_fnid')
        read_only_fields = ['fnid']