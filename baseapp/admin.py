from django.contrib import admin
from .models import * 

@admin.register(Projects)
class ProjectstAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','author','created','update','img','description')
    prepopulated_fields = {"slug":("title",)}

