from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from importlib import import_module
from django.core.urlresolvers import clear_url_caches
from django.db import models
from django.apps import apps
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import login,logout
# Create your views here.
from .models import otp_data
import random
import requests
@login_required
def verify_mobile(request):
	error_message=''
	otp_data_row=otp_data.objects.get(refrence_id=str(request.user))
	print otp_data_row.refrence_id
	if(request.method=="GET"):
		json={"number":otp_data_row.number,"error":error_message}
		if request.user.is_authenticated():
			login_display='<li><a href="/logout">Logout</a></li>'
			login_display2=''
		else:
			login_display='<li><a href="/register">Register</a></li>'
			login_display2='<li><a href="/login">Login</a></li>'
		json['login_display']=login_display,
		json['login_display2']=login_display2,
		return render(request,'mobile/mobile.html',json)
	if(request.method=="POST"):
		if request.POST.get("send")=='SEND':
			n=random.randint(1000,9999)
			setattr(otp_data_row,'otp',n)
			otp_data_row.save()
			
			url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			url+=str(otp_data_row.number)
			#url+='&message='+'E-Cell team welcomes you. \nVerification code for the app is '+otp
			url+='&message='+'Verification code is '+str(n)
			url+='&sender=mNavmo&route=4'
			print requests.request('GET', url)
			json={"number":otp_data_row.number,"error":error_message}
			if request.user.is_authenticated():
				login_display='<li><a href="/logout">Logout</a></li>'
				login_display2=''
			else:
				login_display='<li><a href="/register">Register</a></li>'
				login_display2='<li><a href="/login">Login</a></li>'
			json['login_display']=login_display,
			json['login_display2']=login_display2,	
			return render(request,'mobile/mobile.html',json)
		if request.POST.get("verify")=='VERIFY':
			print"command in verify"
			code_recived=request.POST.get("code")
			print code_recived,otp_data_row.otp

			if(int(code_recived)==int(otp_data_row.otp)):
				setattr(otp_data_row,'flag',1)
				otp_data_row.save()
				return HttpResponseRedirect('/home')
			else:
				error_message="otp did not match Try Again"
				json={"number":otp_data_row.number,"error":error_message}
				if request.user.is_authenticated():
					login_display='<li><a href="/logout">Logout</a></li>'
					login_display2=''
				else:
					login_display='<li><a href="/register">Register</a></li>'
					login_display2='<li><a href="/login">Login</a></li>'
				json['login_display']=login_display,
				json['login_display2']=login_display2,
				return render(request,'mobile/mobile.html',json)