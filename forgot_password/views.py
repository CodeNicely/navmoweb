from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from register.models import user_data
import requests
from random import randint
from forgot_password.models import password_reset_otp
from register.models import user_data
from django.contrib.auth.models import User
# Create your views here.
def forgot_password(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/home")
	else:
		if(request.method=="GET"):
			login_display='<li><a href="/register">Register</a></li>'
			login_display2='<li><a href="/login">Login</a></li>'
			return render(request,'forgot_password/forgot_password.html',{"login_display":login_display,"login_display2":login_display2})
		else:
			if(str(request.POST.get('forgot_password'))=='forgot_password'):
				refrence_id=request.POST.get('reference_id')
				print refrence_id
				otp=randint(99999,999999)
				try:
					user=password_reset_otp.objects.get(refrence_id=refrence_id)
					setattr(user,'otp',otp)
					setattr(user,'flag',0)
					user.save()
					print"try"
				except:
					user_detail=user_data.objects.get(refrence_id=refrence_id)
					print "except"

					password_reset_otp.objects.create(refrence_id=refrence_id,number=user_detail.number,otp=otp,flag=0)
				

				user_data_all=user_data.objects.get(refrence_id=refrence_id)
				url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
				url+=user_data_all.number
				print "31"
				#url+='&message='+'E-Cell team welcomes you. \nVerification code for the app is '+otp
				url+='&message= Hello '+user_data_all.first_name+' Your otp for password reset is '+str(otp)+' and reference id is '+refrence_id
				url+='.'+'&sender=mNavmo&route=4'
				print requests.request('GET',url)


				login_display='<li><a href="/register">Register</a></li>'
				login_display2='<li><a href="/login">Login</a></li>'
				print"end"
				json={}

				json["login_display"]=login_display
				json["login_display2"]=login_display2
				json["reference_id"]=refrence_id
				return render(request,'change_password/change_password.html',json)
			if(str(request.POST.get('change_password'))=='change_password'):
			
				print "rid",request.POST.get('rid')
				refrence_id=request.POST.get('rid')
				print "otp",request.POST.get('otp')
				print "password",request.POST.get('new_password')
				print request.POST.get('rid')
				

				otp_data=password_reset_otp.objects.get(refrence_id=refrence_id)			

				if(int(request.POST.get('otp'))==int(otp_data.otp)):
					print "otp_matched"
					u = User.objects.get(username=refrence_id)
					u.set_password(request.POST.get('new_password'))
					u.save()	
					setattr(otp_data,'flag',1)
					otp_data.save()
					print "Password Changed"
					login_display='<li><a href="/register">Register</a></li>'
					login_display2='<li><a href="/login">Login</a></li>'			
					return HttpResponseRedirect('/')
				else:
					login_display='<li><a href="/register">Register</a></li>'
					login_display2='<li><a href="/login">Login</a></li>'			
					return render(request,'change_password/change_password.html',{"login_display":login_display,"login_display2":login_display2,"error_message":"Your otp did not match please try again !"})
			