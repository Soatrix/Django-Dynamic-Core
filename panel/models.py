from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class Theme(models.Model):
    name = models.CharField(max_length=255)
    light_css = models.TextField(blank=True)
    dark_css = models.TextField(blank=True)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.default:
            # Ensure only one Theme can be default
            Theme.objects.filter(default=True).update(default=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name.title()
