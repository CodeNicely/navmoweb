from __future__ import unicode_literals

from django.db import models

# Create your models here.
class gallery_data(models.Model):
    image=models.ImageField(upload_to='/root/navmo/media/gallery/',default="/media/default.png")
    caption=models.CharField(max_length=512,null=True,blank=True)