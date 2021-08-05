from django.db import models


class ParsedUrl(models.Model):
    url = models.URLField()
    emails = models.ManyToManyField("ParsedEmail")


class ParsedEmail(models.Model):
    email = models.EmailField()
