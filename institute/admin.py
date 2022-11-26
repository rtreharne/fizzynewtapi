from django.contrib import admin
from institute.models import Institute, SessionType

class InstituteAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'name')

class SessionTypeAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'institute_fnid', 'label')

admin.site.register(Institute, InstituteAdmin)
admin.site.register(SessionType, SessionTypeAdmin)
