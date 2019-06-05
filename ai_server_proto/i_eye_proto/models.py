from django.db import models


# Create your models here.
class Checklist(models.Model):
    reserved = models.CharField(max_length=100, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='i_eye_proto', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
