from django.contrib import admin

# Register your models here.
from logs.models import RawLogs


@admin.register(RawLogs)
class RawLogsAdmin(admin.ModelAdmin):
    list_display = [fields.name for fields in RawLogs._meta.fields]