from django.contrib import admin
from course.models import Course, CourseInstance, CourseStudent
from institute.models import Institute

class CourseAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'code', 'name', 'institute', 'visible')

    def institute(self, obj):
        institute_obj = Institute.objects.get(fnid=obj.institute_fnid)
        return institute_obj

class CourseInstanceAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'course', 'start', 'duration_weeks')

    def course(self, obj):
        course_obj = Course.objects.get(fnid=obj.course_fnid)
        return course_obj

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseInstance, CourseInstanceAdmin)
admin.site.register(CourseStudent)

