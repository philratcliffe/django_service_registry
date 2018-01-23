from django.db import models

class Service(models.Model):
    name = models.CharField (max_length=255)
    version = models.CharField(max_length=14)

    def __str__(self):
        return "{}:{}".format(self.name, self.version)
