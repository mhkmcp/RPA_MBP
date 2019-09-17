from django.db import models


# Create your models here.


class Organizations(models.Model):
    STATUS = (
        (u'A', u'ACTIVE'),
        (u'I', u'INACTIVE'),
        (u'P', u'PROCESSING'),
    )

    CATEGORY = (
        (u'B', u'BANK'),
        (u'H', u'HEALTH'),
    )

    organization_name = models.CharField("Organization Name", max_length=150, blank=False, null=False)
    organization_slug = models.CharField("Slug", max_length=20, blank=False, null=False)
    organization_status = models.CharField("Status", max_length=1, choices=STATUS, blank=True, null=True,
                                           default=STATUS[0][0])
    organization_category = models.CharField("Category", max_length=1, choices=CATEGORY, blank=True, null=True,
                                             default=CATEGORY[0][0])
