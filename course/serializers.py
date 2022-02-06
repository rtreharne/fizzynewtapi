from rest_framework.serializers import ModelSerializer
from course.models import Course

class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = ('fnid', 'institute_fnid', 'code', 'name', 'visible')
        read_only_fields = ['fnid']