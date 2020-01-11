from __future__ import unicode_literals

from django.db import models


# Create your models here.


# Create your models here.



class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
