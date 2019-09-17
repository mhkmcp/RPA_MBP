from django.contrib import admin

# Register your models here.
from .models import Organizations


@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = [fields.name for fields in Organizations._meta.fields]