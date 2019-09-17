from django.db import models


# Create your models here.


class RawLogs(models.Model):
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True, blank=True, null=True)
    process_name = models.CharField("Process Name", max_length=100, blank=False, null=False)
    log_message = models.CharField("Log Message", max_length=500, blank=False, null=False)
