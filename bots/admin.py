from django.contrib import admin

# Register your models here.
from bots.models import BotConfig


@admin.register(BotConfig)
class BotConfigAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BotConfig._meta.fields]