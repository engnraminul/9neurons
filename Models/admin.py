from django.contrib import admin
from .models import Category, Model, Files, Sub_Category



class FilesAdmin(admin.StackedInline):
    model = Files

class ModelAdmin(admin.ModelAdmin):
    inlines = [FilesAdmin]

admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Model, ModelAdmin)
admin.site.register(Files)