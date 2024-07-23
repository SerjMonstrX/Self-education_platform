from django.contrib import admin
from .models import Section, Material


@admin.register(Section)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public')
    list_filter = ('owner',)
    search_fields = ('owner', 'title')


@admin.register(Material)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public', 'section')
    list_filter = ('owner', 'section')
    search_fields = ('owner', 'title', 'section')