from django.contrib import admin
from .models import Task, Workspace, Notification

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description', 'owner__username')
    filter_horizontal = ('members',)
    date_hierarchy = 'created_at'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'workspace', 'created_by', 'assigned_to', 
                   'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'workspace', 'due_date')
    search_fields = ('title', 'description', 'created_by__username', 
                    'assigned_to__username')
    date_hierarchy = 'due_date'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'workspace')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'task__title', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
