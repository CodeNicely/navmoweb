from django.contrib import admin
from forgot_password.models import password_reset_otp

# Register your models here.

class forgot_password(admin.ModelAdmin):
    list_display=["refrence_id","otp","number","flag"]
admin.site.register(password_reset_otp,forgot_password)