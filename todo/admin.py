from django.contrib import admin
from .models import ToDo, Project

class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(ToDo, ToDoAdmin)
admin.site.register(Project)

