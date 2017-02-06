from __future__ import unicode_literals

from django.db import models

# Create your models here.
class admit_card_data(models.Model):
	refrence_id=models.CharField(max_length=10,blank=True,null=True)
	date=models.CharField(max_length=120,blank=True,null=True)
	time=models.CharField(max_length=120,blank=True,null=True)
	center=models.CharField(max_length=120,blank=True,null=True)
	city=models.CharField(max_length=120,blank=True,null=True)
	

class second_round_admit_card_data(models.Model):
	refrence_id=models.CharField(max_length=10,blank=True,null=True)
	ROUND_CHOICES = (
    ('First', "First Round"),
    ('Semi-Finals', "Semi Finals"),
    ('Finals', "Finals")

)
# 	CENTER_CHOICES = (
#     ('NH Goel School Raipur', "NH Goel School Raipur"),
#     ('Sambalpur, Udisha', "Sambalpur, Udisha"),
#     ('ICIS, Bhosari, Pune', "ICIS, Bhosari, Pune"),
#     ('Atlier School Magarpatta', "Atlier School Magarpatta"),
#     ('NBIS Rajnandgaon', "NBIS Rajnandgaon"),
#     ('NPPS Rajnandgaon', "NPPS Rajnandgaon"),
#     ('None',"None"),

# )	
	current_round=models.CharField(choices=ROUND_CHOICES,max_length=120,blank=True,null=True)
	gamma_group_one=models.BooleanField(default=False)
	alpha_beta_theta_group_two=models.BooleanField(default=False)
	# exam_center=models.CharField(choices=CENTER_CHOICES,max_length=120,blank=True,null=True,default=None)
	exam_center=models.CharField(max_length=120,blank=True,null=True,default=None)
