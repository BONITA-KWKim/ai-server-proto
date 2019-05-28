from django.db import models


# Create your models here.
class Checklist(models.Model):
    reserved = models.CharField(max_length=100, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
