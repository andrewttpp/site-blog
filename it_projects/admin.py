from django.contrib import admin

from .models import *


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('title',)
    list_editable = ('is_published', )
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Category, CategoryAdmin)
