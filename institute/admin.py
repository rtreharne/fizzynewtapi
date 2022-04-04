from django.contrib import admin
from institute.models import Institute

class InstituteAdmin(admin.ModelAdmin):
    list_display = ('fnid', 'name')

admin.site.register(Institute, InstituteAdmin)
