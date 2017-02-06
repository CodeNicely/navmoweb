from __future__ import unicode_literals

from django.db import models

class user_data(models.Model):
    refrence_id=models.CharField(max_length=10,blank=True,null=True)
    first_name=models.CharField(max_length=120,blank=True,null=True)
    last_name=models.CharField(max_length=120,blank=True,null=True)
    number=models.CharField(max_length=120,blank=True,null=True)
    email=models.CharField(max_length=120,blank=True,null=True)
    parent_father=models.CharField(max_length=120,blank=True,null=True)
    parent_mother=models.CharField(max_length=120,blank=True,null=True)
    dob=models.CharField(max_length=120,blank=True,null=True)
    tshirt_size=models.CharField(max_length=120,blank=True,null=True)
    address=models.CharField(max_length=120,blank=True,null=True)
    school=models.CharField(max_length=120,blank=True,null=True)
    grade=models.CharField(max_length=120,blank=True,null=True)
    gender=models.CharField(max_length=120,blank=True,null=True)
    exam_centre_1=models.CharField(max_length=120,blank=True,null=True)
    exam_centre_2=models.CharField(max_length=120,blank=True,null=True)
    exam_group_1=models.CharField(max_length=120,blank=True,null=True)
    exam_group_2=models.CharField(max_length=120,blank=True,null=True)
    flag_exam_centre_1=models.PositiveSmallIntegerField(default=0)
    flag_exam_centre_2=models.PositiveSmallIntegerField(default=0)
    flag_exam_group_1=models.PositiveSmallIntegerField(default=0)
    flag_exam_group_2=models.PositiveSmallIntegerField(default=0)
    flag_workshop=models.PositiveSmallIntegerField(default=0)
    flag_mpe_student=models.PositiveSmallIntegerField(default=0)
    image=models.ImageField(upload_to='/media/user_images/',default="/media/default.png")

class exam_center_data(models.Model):
    exam_center=models.CharField(max_length=100,blank=True,null=True)


class results_data(models.Model):
    reference_id=models.CharField(max_length=10,blank=False,null=False)

class topper_data(models.Model):
    reference_id= models.CharField(max_length=120,blank=False,null=False)
    GROUP_CHOICES= (('alpha','alpha'),('beta','beta'),('thetha','thetha'),('gamma','gamma'))
    group=models.CharField(max_length=120,blank=True,choices=GROUP_CHOICES)
    ROUND_CHOICES = (
    ('Semi-Finals', "Semi-Finals"),
    ('Finals', "Finals"))
    current_round=models.CharField(choices=ROUND_CHOICES,max_length=120,blank=True,null=True)
    LEVEL_CHOICES= (('alpha','alpha'),('alpha1','ALPHA 1'),('alpha2','alpha2'),('beta1','beta1'),('beta2','beta2'),('beta3','beta3'),('beta4','beta4'),('beta5','beta5'),('MM-1','MM-1'),('MM-1A','MM-1A'),('MM-1B','MM-1B'),('MM-1C','MM-1C'),('MM-2','MM-2'),('MM-3','MM-3'),('MM-4','MM-4'),('MM-5','MM-5'),('thetha-1','thetha-1'),('thetha-2','thetha-2'))
    CENTER_CHOICES = (
    ('NH Goel', "NH Goel"),
    ('MPE Odisha', "MPE Odisha"),
    ('MPE Ranchi', "MPE Ranchi"),
    ('ICIS', "ICIS"),
    ('MPE Raipur', "MPE Raipur"),
    ('B K Birla', "B K Birla"),
    ('NPPS , Rajnandgaon', "NPPS , Rajnandgaon"),
    ('NBIS , Rajnandgaon', "NBIS , Rajnandgaon"),
    ('Atelier School Magarpatta', "Atelier School Magarpatta"),
    ('MPE KOTA', "MPE KOTA"),
    ('MPE AMRAVATI', "MPE AMRAVATI"),
    ('MPE KHARADI', "MPE KHARADI"),
    
    )
    AWARD_CHOICES = (
    ('School Gold Medal', "School Gold Medal "),
    ('School Silver Medal ', "School Silver Medal "),
    ('School Bronze Medal ', "School Bronze Medal "),
    )
    center=models.CharField(max_length=120,blank=True,choices=CENTER_CHOICES,default='NH Goel')
    rank=models.CharField(max_length=120,blank=False,null=True)
    medal=models.CharField(choices=AWARD_CHOICES,max_length=120,blank=False,null=True)

class marks_data(models.Model):
    reference_id= models.CharField(max_length=120,blank=False,null=False)
    GROUP_CHOICES= (('alpha','alpha'),('beta','beta'),('thetha','thetha'),('gamma','gamma'))
    group=models.CharField(max_length=120,blank=True,choices=GROUP_CHOICES)
    ROUND_CHOICES = (
    ('First-Round', "First-Round"),
    ('Semi-Finals', "Semi-Finals"),
    ('Finals', "Finals"))
    current_round=models.CharField(choices=ROUND_CHOICES,max_length=120,blank=True,null=True)
    LEVEL_CHOICES= (('alpha','alpha'),('alpha1','alpha1'),('alpha2','alpha2'),('beta1','beta1'),('beta2','beta2'),('beta3','beta3'),('beta4','beta4'),('beta5','beta5'),('MM-1','MM-1'),('MM-1A','MM-1A'),('MM-1B','MM-1B'),('MM-1C','MM-1C'),('MM-2','MM-2'),('MM-3','MM-3'),('MM-4','MM-4'),('MM-5','MM-5'),('thetha-1','thetha-1'),('thetha-2','thetha-2'))
    level=models.CharField(max_length=120,blank=True,choices=LEVEL_CHOICES)
    CENTER_CHOICES = (
    ('NH Goel', "NH Goel"),
     ('MPE Odisha', "MPE Odisha"),
    ('MPE Ranchi', "MPE Ranchi"),
    ('ICIS', "ICIS"),
    ('MPE Raipur', "MPE Raipur"),
    ('B K Birla', "B K Birla"),
    ('NPPS , Rajnandgaon', "NPPS , Rajnandgaon"),
    ('NBIS , Rajnandgaon', "NBIS , Rajnandgaon"),
    ('Atelier School Magarpatta', "Atelier School Magarpatta"),
    ('MPE KOTA', "MPE KOTA"),
    ('MPE AMRAVATI', "MPE AMRAVATI"),
    ('MPE KHARADI', "MPE KHARADI"),


    )
    center=models.CharField(max_length=120,blank=True,choices=CENTER_CHOICES,default='NH Goel')
    marks_first=models.FloatField(blank=False,null=False,default=0.0)
    time_first=models.FloatField(blank=False,null=False,default=0.0)
    marks_semi=models.FloatField(blank=False,null=False,default=0.0)
    time_semi=models.FloatField(blank=False,null=False,default=0.0)
    marks_final=models.FloatField(blank=False,null=False,default=0.0)
    time_final=models.FloatField(blank=False,null=False,default=0.0)    
    npi_first=models.FloatField(blank=False,null=False,default=0.0)
    npi_semi=models.FloatField(blank=False,null=False,default=0.0)
    npi_final=models.FloatField(blank=False,null=False,default=0.0)

class rank_data(models.Model):
    reference_id= models.CharField(max_length=120,blank=False,null=False)
    group=models.CharField(max_length=120,blank=True)
    level=models.CharField(max_length=120,blank=True)
    centre_rank=models.IntegerField(blank=False, null=False, default=0)
    national_level_rank=models.IntegerField(blank=False, null=False, default=0)
    national_group_rank=models.IntegerField(blank=False, null=False, default=0)

# class complete_data(models.Model):
#     reference_id= models.CharField(max_length=120,blank=False,null=False)
#     centre=models.CharField(max_length=50,blank=False,null=False)
#     name=models.CharField(max_length=150,blank=False,null=False)
#     father=models.CharField(max_length=150,blank=False,null=False)
#     school=models.CharField(max_length=120,blank=True,null=True)
#     mob=models.CharField(max_length=120,blank=True,null=True)
#     email=models.CharField(max_length=120,blank=True,null=True)
#     grade=models.CharField(max_length=120,blank=True,null=True)
#     group=models.CharField(max_length=120,blank=True)
#     level=models.CharField(max_length=120,blank=True)
#     current_round=models.CharField(max_length=120,blank=True,null=True)
#     marks=models.FloatField(blank=False,null=False,default=0.0)
#     time=models.FloatField(blank=False,null=False,default=0.0)
#     npi=models.FloatField(blank=False,null=False,default=0.0)
#     centre_rank=models.IntegerField(blank=False, null=False, default=0)
#     national_level_rank=models.IntegerField(blank=False, null=False, default=0)
#     national_group_rank=models.IntegerField(blank=False, null=False, default=0)
#     certificate=models.CharField(max_length=150,blank=True,null=True)
#     trophy=CharField(max_length=150,blank=True,null=True)

        
