from django.contrib import admin
from .models import *
# Register your models here.
class gallery_dataAdmin(admin.ModelAdmin):
	list_display=['id','image','caption']
admin.site.register(gallery_data,gallery_dataAdmin)