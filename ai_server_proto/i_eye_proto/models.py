from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.
class Diagnosis(models.Model):
    user_id = models.CharField(max_length=100, blank=True, default='')
    '''
    label = JSONField()
    best_guess = JSONField()
    web_entities = JSONField()
    diagnosis = JSONField()
    '''
    label = models.CharField(max_length=1000, blank=True, default='')
    best_guess = models.CharField(max_length=1000, blank=True, default='')
    web_entities = models.CharField(max_length=1000, blank=True, default='')
    diagnosis = models.CharField(max_length=1000, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='i_eye_proto', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)


class EyeImage(models.Model):
    user_id = models.CharField(max_length=100, blank=True, default='')
    eye_photo = models.ImageField(upload_to='pic_folder/', default='pic_folder/None/no-img.jpg')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
