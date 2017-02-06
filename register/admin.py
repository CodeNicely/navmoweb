from django.contrib import admin
from .models import *
from .models import marks_data

# Register your models here.
class user_dataAdmin(admin.ModelAdmin):
    list_display=["id","refrence_id","first_name","last_name","number","email","parent_father","parent_mother","dob","tshirt_size","address","school","grade","gender","exam_centre_1","exam_centre_2","exam_group_1","exam_group_2","flag_exam_group_1","flag_exam_group_2","flag_workshop"]
admin.site.register(user_data,user_dataAdmin)

class exam_center_dataAdmin(admin.ModelAdmin):
    list_display=["exam_center"]
admin.site.register(exam_center_data,exam_center_dataAdmin)

class results_dataAdmin(admin.ModelAdmin):
    list_display=["reference_id"]
admin.site.register(results_data,results_dataAdmin)

class topper_dataAdmin(admin.ModelAdmin):
    list_display=["reference_id","group","current_round","center","rank","medal"]
admin.site.register(topper_data,topper_dataAdmin)

class marks_dataAdmin(admin.ModelAdmin):
	list_display=["reference_id","group","current_round","level","center","marks_first","time_first","marks_semi","time_semi","marks_final","time_final","npi_first","npi_semi","npi_final"]
admin.site.register(marks_data,marks_dataAdmin)

class rank_dataAdmin(admin.ModelAdmin):
	list_display=["reference_id","level","centre_rank","national_level_rank", "national_group_rank"]
admin.site.register(rank_data, rank_dataAdmin)
