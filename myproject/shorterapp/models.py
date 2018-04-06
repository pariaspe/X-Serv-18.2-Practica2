from django.db import models

# Create your models here.

class URLs(models.Model):
    url = models.URLField()
    def __str__(self):
        return self.url
