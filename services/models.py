"""
Service model.
"""

__author__ = 'Phil Ratcliffe'

from django.db import models

from .validators import validate_service, validate_version


class Service(models.Model):
    service = models.CharField(max_length=128, validators=[validate_service])
    version = models.CharField(max_length=8, validators=[validate_version])

    def __str__(self):
        return "{}:{}".format(self.service, self.version)
