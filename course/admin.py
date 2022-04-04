from django.contrib import admin
from course.models import Course
from institute.models import Institute

class CourseAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'code', 'name', 'institute', 'visible')

    def institute(self, obj):
        institute_obj = Institute.objects.get(fnid=obj.institute_fnid)
        return institute_obj

admin.site.register(Course, CourseAdmin)
