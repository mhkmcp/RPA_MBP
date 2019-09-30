from django.db import models

# Create your models here.


class BotConfig(models.Model):
    config_class = models.CharField("Config Class", max_length=30, blank=True, null=True)
    config_tag = models.CharField("Config Tag", max_length=30, blank=True, null=True)
    config_settings = models.CharField("Settings String", max_length=200, blank=True, null=True)