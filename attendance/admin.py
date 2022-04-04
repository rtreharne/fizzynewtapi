from django.contrib import admin
from attendance.models import Code, SessionType, Session, Attendance
from course.models import Course
from student.models import Student

class SessionTypeAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'name')

class CodeAdmin(admin.ModelAdmin):
    list_display = ('code',)
    search_fields = ('code',)

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_start', 'session_code', 'course', 'average_attendance', 'confirmed')

    def course(self, obj):
        course_obj = Course.objects.get(fnid=obj.course_fnid)
        return "{} - {}".format(course_obj.code, course_obj.name)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('updated_at', 'student', 'course', 'session_code', 'student_code', 'present', 'verified')

    def student(self, obj):
        student_obj = Student.objects.get(fnid=obj.student_fnid)
        return student_obj

    def course(self, obj):
        course_obj = Course.objects.get(fnid=obj.course_fnid)
        return course_obj





admin.site.register(Code, CodeAdmin)
admin.site.register(SessionType, SessionTypeAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Attendance, AttendanceAdmin)
