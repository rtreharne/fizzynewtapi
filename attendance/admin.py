from django.contrib import admin
from attendance.models import SessionRequest, Attendance

class SessionRequestAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'institute_fnid', 'course_instance_fnid')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'institute_fnid', 'course_instance_fnid', 'student_fnid', 'present')


admin.site.register(SessionRequest, SessionRequestAdmin)
admin.site.register(Attendance, AttendanceAdmin)