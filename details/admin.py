from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(College)
admin.site.register(Teacher)
admin.site.register(Note)
admin.site.register(Year)
admin.site.register(Subject)
admin.site.register(Topic)
# admin.site.register(Department)
admin.site.register(File)
admin.site.register(Part)

class CollegeInline(admin.TabularInline):
    model = College

class DepartmentAdmin(admin.ModelAdmin):
    inlines = [
        CollegeInline,
    ]
admin.site.register(Department,DepartmentAdmin)


# class SubjectInline(admin.TabularInline):
#     model = Subject

# class TopicAdmin(admin.ModelAdmin):
#     inlines = [SubjectInline]

# admin.site.register(Topic,TopicAdmin) 

