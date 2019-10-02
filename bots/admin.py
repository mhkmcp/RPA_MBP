from django.contrib import admin

# Register your models here.
from bots.models import BotConfig, BotConfigNid, BotConfigCbs


@admin.register(BotConfig)
class BotConfigAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BotConfig._meta.fields]


@admin.register(BotConfigNid)
class BotConfigNidAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BotConfigNid._meta.fields]


@admin.register(BotConfigCbs)
class BotConfigCbsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BotConfigCbs._meta.fields]
