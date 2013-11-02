from django.contrib import admin
from myproject.googleapi.models import *


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('dateTime', 'title')
    search_fields = ('dateTime', 'title')
    
admin.site.register(UserInfo)
admin.site.register(Project, ProjectAdmin)
admin.site.register(FormInput)
admin.site.register(BackImage)
admin.site.register(TurnOn)