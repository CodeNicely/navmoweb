from __future__ import unicode_literals

from django.db import models

# Create your models here.
class password_reset_otp(models.Model):
    refrence_id=models.CharField(max_length=10,blank=True,null=True)
    number=models.BigIntegerField(blank=False,null=False,default=0)
    otp=models.BigIntegerField(default=0)
    flag=models.PositiveSmallIntegerField(default=0)

