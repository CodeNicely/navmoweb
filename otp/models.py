from __future__ import unicode_literals

from django.db import models


class otp_data(models.Model):
    refrence_id=models.CharField(max_length=10,blank=True,null=True)
    number=models.CharField(max_length=120,blank=True,null=True)
    otp=models.PositiveSmallIntegerField(default=0)
    flag=models.PositiveSmallIntegerField(default=0)

