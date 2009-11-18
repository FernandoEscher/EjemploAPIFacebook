from django.db import models
from django.contrib.auth.models import User

class FacebookUser(models.Model):
    fb_uid = models.CharField(max_length=200, verbose_name='Facebook username', blank=True)
    session = models.CharField(max_length=200, verbose_name='Facebook session key', blank=True) 
    secret = models.CharField(max_length=200, verbose_name='Facebook secret key', blank=True)
