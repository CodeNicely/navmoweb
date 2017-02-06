from django.contrib import admin
from .models import *
# Register your models here.
class payment_dataAdmin(admin.ModelAdmin):
    list_display=["refrence_id","amount","domain_type","last_transaction_id","flag"]
admin.site.register(payment_data,payment_dataAdmin)

class domain_dataAdmin(admin.ModelAdmin):
	list_display=["domain_type","name","amount"]
admin.site.register(domain_data,domain_dataAdmin)