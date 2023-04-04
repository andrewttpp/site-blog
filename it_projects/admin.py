from django.contrib import admin

from .models import *


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'time_create', 'photo', 'author_setting', 'is_published')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'time_create')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_display_links = ('email',)


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)

