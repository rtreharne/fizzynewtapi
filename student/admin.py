from django.contrib import admin
from student.models import Student
from school.models import School
from institute.models import Institute
from programme.models import Programme

class StudentAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'last_name', 'first_name', 'institute', 'school', 'programme', 'international', 'verified')


    def school(self, obj):
        school_obj = School.objects.get(fnid=obj.school_fnid)
        return  school_obj

    def institute(self, obj):
        institute_obj = Institute.objects.get(fnid=obj.institute_fnid)
        return institute_obj

    def programme(self, obj):
        programme_obj = Programme.objects.get(fnid=obj.programme_fnid)
        return programme_obj





admin.site.register(Student, StudentAdmin)
