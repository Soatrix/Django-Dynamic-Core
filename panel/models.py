from django.db import models

# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=255)
    light_css = models.TextField(blank=True)
    dark_css = models.TextField(blank=True)

    def __str__(self):
        return self.name.title()