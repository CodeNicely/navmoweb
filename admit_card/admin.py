from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.
class admit_card_dataAdmin(admin.ModelAdmin):
    list_display=["refrence_id","date","center","city"]
admin.site.register(admit_card_data,admit_card_dataAdmin)

class second_round_admit_card_dataAdmin(admin.ModelAdmin):
    list_display=["refrence_id","current_round","gamma_group_one","alpha_beta_theta_group_two",]
admin.site.register(second_round_admit_card_data,second_round_admit_card_dataAdmin)
