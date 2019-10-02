from django.db import models


# Create your models here.


class BotConfig(models.Model):
    config_class = models.CharField("Config Class", max_length=30, blank=True, null=True)
    config_tag = models.CharField("Config Tag", max_length=30, blank=True, null=True)
    config_settings = models.CharField("Settings String", max_length=200, blank=True, null=True)
    config_validity = models.BooleanField("Config Validity", default=True, blank=True, null=True)


class BotConfigNid(models.Model):
    nid_url = models.URLField("NID URL", blank=False, null=False)
    nid_username = models.CharField("NID Username", max_length=20, blank=False, null=False)
    nid_password = models.CharField("NID Password", max_length=20, blank=False, null=False)
    config_validity = models.BooleanField("Config Validity", default=True, blank=True, null=True)


class BotConfigCbs(models.Model):
    cbs_url = models.URLField("CBS URL", blank=False, null=False)
    cbs_username = models.CharField("CBS Username", max_length=20, blank=False, null=False)
    cbs_password = models.CharField("CBS Password", max_length=20, blank=False, null=False)
    config_validity = models.BooleanField("Config Validity", default=True, blank=True, null=True)
