from django.contrib import admin

# Register your models here.
from webapp.models import Task, StatusModel, TypeModel, Project


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'detailed_description', 'created_at', 'project']
    list_filter = ['created_at']
    search_fields = ['statuses', 'types']
    fields = ['description', 'detailed_description', 'project', 'statuses', 'types', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)
admin.site.register(StatusModel)
admin.site.register(Project)
admin.register(TypeModel)
