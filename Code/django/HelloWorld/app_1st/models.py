from __future__ import unicode_literals

from django.db import models

# Create your models here.


class FirstClass(models.Model):
    class_name = models.CharField(max_length=100)
    create_date = models.DateTimeField('date published')


class SecondClass(models.Model):
    first = models.ForeignKey(FirstClass, on_delete=models.CASCADE)
    second_text = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
