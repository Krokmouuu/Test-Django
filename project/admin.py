from django.contrib import admin
from .models import Project, Tag


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'completed')

    list_filter = ('completed', 'due_date')

    search_fields = ('title', 'description')

    ordering = ('-due_date',)

    date_hierarchy = 'due_date'

    list_per_page = 20 # To display X projects per page for big projects

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'completed', 'due_date', 'image') # To display the fields in the admin panel
        }),
    )

class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)

    search_fields = ('title',)

    ordering = ('title',)

    fieldsets = (
        (None, {
            'fields': ('title', 'projects')
        }),
    )

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag, TagAdmin)