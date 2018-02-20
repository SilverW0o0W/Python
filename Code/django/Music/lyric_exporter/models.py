from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Lyric(models.Model):
    song_id = models.CharField(primary_key=True, max_length=12)
    last_modified = models.DateField(auto_now=True)
    locate_path = models.CharField(max_length=300)
