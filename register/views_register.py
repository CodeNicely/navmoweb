from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.template import RequestContext
from .models import *
from importlib import import_module
from django.core.urlresolvers import clear_url_caches
from django.db import models
from django.db.models import Max
from django.apps import apps
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import login,logout
from otp.models import otp_data
from payment.models import payment_data
import random
import os
from .models import exam_center_data
from .models import results_data
from django.core.urlresolvers import reverse
import requests
from django.core.mail import send_mail
from admit_card.models import *
import json
from django.db.models import Q
from . models import rank_data

def login_check(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    else:
        return login(request)
        
@csrf_exempt
def registration(request):	
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
		
		json={
		'login_display':login_display,
		'login_display2':login_display2,
		}
		
		return HttpResponseRedirect('/logout_and_register/',json)
	if(request.method=="GET"):
		json={}
		list_data=''
		for o in exam_center_data.objects.all():
			list_data+='<option value="'+o.exam_center+'">'+o.exam_center+'</option>'
			print o,o.exam_center
			print list_data
		json['list_data']=list_data
		return render(request,'registration/registration.html',json)
	if(request.method=="POST"):
		
		firstname=str(request.POST.get('firstname'))
		print firstname
		lastname=str(request.POST.get('lastname'))
		print lastname
		fathername=str(request.POST.get('fathername'))
		print fathername
		mothername=str(request.POST.get('mothername'))
		print mothername
		dob=str(request.POST.get('dob'))
		print dob
		gender=str(request.POST.get('gender'))
		print gender
		tsize=str(request.POST.get('tsize'))
		print tsize
		examcenter=str(request.POST.get('exam_center'))
		print examcenter
		examcenterr=str(request.POST.get('exam_centerr'))
		print examcenterr
		email=str(request.POST.get('email'))
		print email
		pnum=str(request.POST.get('pnum'))
		print pnum
		address=str(request.POST.get('address'))
		print address
		school=str(request.POST.get('school'))
		print school
		sclass=str(request.POST.get('class'))
		print sclass
		exam_group_1=str(request.POST.get('group_exam_field1'))
		print exam_group_1
		exam_group_2=str(request.POST.get('group_exam_field2'))
		print exam_group_2
		first_preference=str(request.POST.getlist('first'))
		print first_preference
		print 'First '+str(request.POST.get('first'))
		print str(request.POST.get('second_preference'))
		print str(request.POST.get('first_school'))
		print str(request.POST.get('second_school'))

		first_choice=str(request.POST.get('first_school'))
		print first_choice
		second_choice=str(request.POST.get('second_school'))
		print second_choice
		second_preference=str(request.POST.get('second_preference'))
		print second_preference
		workshop=str(request.POST.get('workshop'))
		print workshop
		mpe=str(request.POST.get('mpe_student'))
		print mpe
		gender=str(request.POST.get('gender'))
		print gender
		flag_group_exam1=str(request.POST.get('group_exam1'))
		print flag_group_exam1
		flag_group_exam2=str(request.POST.get('group_exam2'))
		print flag_group_exam2
		
		if exam_group_1=='None':
			flag_group_exam1=0
		else:
			flag_group_exam1=1


		if exam_group_2=='None':
			flag_group_exam2=0
		else:
			flag_group_exam2=1


		# if flag_group_exam1 == 'None':
		# 	flag_group_exam1='0'
		
		# if flag_group_exam2 == 'None':
		# 	flag_group_exam2='0'
		


		try:
			image=request.FILES.get('pic').name
			while True:
				try:
					folder = 'media/'+this_refrence_id+'/'
					os.mkdir(os.path.join(folder))
					break
				except:
					this_refrence_id=str(int(this_refrence_id)+1)
			# full_filename = os.path.join(folder, image)
			# print "full name",full_filename
			#fout = open(folder+image, 'wb+')
			print "image=",image
			fout = open(folder+image, 'w')
			file_content = request.FILES.get('pic').read()
			#for chunk in file_content.chunks():
			fout.write(file_content)
			fout.close()
		except Exception,e:
			image='image'
			print e

		# if(int(mpe)==1):
		# 	mpe_flag=1
		# else:
		# 	mpe_flag=0
		this_refrence_id=str(int(user_data.objects.all().last().refrence_id)+1)

		if mpe=='Yes':
			mpe_flag=1
		else:
			mpe_flag=0

		if workshop=='Yes':
			workshop=1
		else:
			workshop=0

		user_data.objects.create(
			exam_group_1=exam_group_1,
			exam_group_2=exam_group_2,
			flag_exam_group_1=int(flag_group_exam1),
			flag_exam_group_2=int(flag_group_exam2),
			refrence_id=this_refrence_id,
			first_name=firstname,
			last_name=lastname,
			number=pnum,
			email=email,
			parent_father=fathername,
			parent_mother=mothername,
			dob=dob,
            tshirt_size=tsize,
            address=address,
            school=school,
            grade=sclass,
            exam_centre_1=examcenter,
            exam_centre_2=examcenterr,
            flag_mpe_student=mpe_flag,
            flag_exam_centre_1=int(first_choice),
            flag_exam_centre_2=int(second_choice),
            flag_workshop=int(workshop),
            gender=gender,
            image=this_refrence_id+'/'+image
            )
		print user_data.objects.get(refrence_id=this_refrence_id)
		
		# Send Reference id to user mobiles

		url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
		url+=pnum
		#url+='&message='+'E-Cell team welcomes you. \nVerification code for the app is '+otp
		url+='&message='+'Thanks for Registring with Navmo - Your Reference id is '+this_refrence_id
		url+='. It will be used for login anytime with your password. :)'+'&sender=mNavmo&route=4'
		print requests.request('GET', url)
		
		url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
		url+='8446019312'
		#url+='&message='+'E-Cell team welcomes you. \nVerification code for the app is '+otp
		url+='&message='+'New User Registered With Navmo with Reference id is '+this_refrence_id
		url+='.'+'&sender=mNavmo&route=4'
		print requests.request('GET', url)
				
		


		User.objects.create_user(
			username=this_refrence_id,
			password=request.POST.get('password'),
			email=email,
			)
		if request.user.is_authenticated():
			login_display='<li><a href="/logout">Logout</a></li>'
			login_display2=''
		
		else:
			login_display=''
			login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'

		n=random.randint(1000,9999)
		
		if ((int(flag_group_exam1)==1)and(int(flag_group_exam2)==0)):
			domain_type=1
		if ((int(flag_group_exam1)==0)and(int(flag_group_exam2)==1)):
			domain_type=2
		if ((int(flag_group_exam1)==1)and(int(flag_group_exam2)==1)):
			domain_type=3
		if ((int(flag_group_exam1)==1)and(int(flag_group_exam2)==0)and(int(workshop))):
			domain_type=4
		if ((int(flag_group_exam1)==0)and(int(flag_group_exam2)==1)and(int(workshop))):
			domain_type=5
		if ((int(flag_group_exam1)==1)and(int(flag_group_exam2)==1)and(int(workshop))):
			domain_type=6

		payment_data.objects.create(refrence_id=this_refrence_id,flag=0,amount=0,domain_type=domain_type)
		otp_data.objects.create(refrence_id=this_refrence_id,otp=n,flag=0,number=pnum)
		
		message='Please note the refrence id \n this will be used for user login '+str(this_refrence_id)+'\n <a href="\login" >Please login to continue </a>'
		# ##request.flash['login_display']=login_display
		# ##request.flash['login_display2']=login_display2
		# import urllib

		# #url = reverse('/message/', kwargs={'message': message})
		# print urllib.urlencode(message)
		# print aditya
		request.session['message'] = message
		return HttpResponseRedirect('/message')

@login_required
def home(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	print str(request.user)
	if(otp_data.objects.get(refrence_id=str(request.user)).flag==1):
		if(request.method=="POST"):
			if 'payment' in request.POST:
				return HttpResponseRedirect("/payment/")
			if 'level_name' in request.POST:
				get_level=request.POST.get('level_name')
				request.session['level_name']=get_level
				return HttpResponseRedirect("/download_spr_user/")
		user_data_row=user_data.objects.get(refrence_id=str(request.user))
		
		group_1=str(user_data_row.exam_group_1)
		group_2=str(user_data_row.exam_group_2)

		if (user_data_row.flag_exam_group_1==1 and user_data_row.flag_exam_group_2 ==0):
			exam_group = group_1
		elif (user_data_row.flag_exam_group_1==0 and user_data_row.flag_exam_group_2 ==1):
			exam_group = group_2
		else :
			exam_group =  "%s||\n%s" % (group_1,group_2)

		json={
		'image':user_data_row.image.url,
		'refrence_id':user_data_row.refrence_id,
		'first_name':user_data_row.first_name,
	    'last_name':user_data_row.last_name,
	    'number':user_data_row.number,
	    'email':user_data_row.email,
	    'parent_father':user_data_row.parent_father,
	    'parent_mother':user_data_row.parent_mother,
	    'dob':user_data_row.dob,
	    'tshirt_size':user_data_row.tshirt_size,
	    'address':user_data_row.address,
	    'school':user_data_row.school,
	    'grade':user_data_row.grade,
	    'gender':user_data_row.gender,
	    'exam_centre_1':user_data_row.exam_centre_1,
	    'exam_centre_2':user_data_row.exam_centre_2,
	    'flag_workshop':user_data_row.flag_workshop,
	    'flag_mpe_student':user_data_row.flag_mpe_student,
	    'exam_group1':user_data_row.exam_group_1,
	    'exam_group2':user_data_row.exam_group_2,
	    'exam_group':exam_group, 
	    'flag_exam_centre_1':user_data_row.flag_exam_centre_1,
	    'flag_exam_centre_2':user_data_row.flag_exam_centre_2,
	    'login_display':login_display,
	    'login_display2':login_display2,
	    }
	    #as
		if(payment_data.objects.get(refrence_id=str(request.user)).flag==1):
			json['payment_status']="Check Status"
		else:
			json['payment_status']="Pay Now"

		flag=payment_data.objects.get(refrence_id=str(request.user)).flag
		try:
			print"code@290"
			admit_card_data.objects.get(refrence_id=str(request.user))
			print"code@292"
			if(flag==1):
				json['admit_card']="enabled"
			if(flag==0):
				json['admit_card']="disabled"
		except:
			json['admit_card']="disabled"

		spr_group_count=0
		for rank_details in rank_data.objects.filter(reference_id=str(request.user)):
			spr_group_count+=1

		json['spr_group_count']=spr_group_count
		print "No. of group = ",spr_group_count

		if spr_group_count==1:
			for rank_details in rank_data.objects.filter(reference_id=str(request.user)):
				json['group1']=rank_details.level
		else:
			count_flag=0
			for rank_details in rank_data.objects.filter(reference_id=str(request.user)):
				if count_flag==0:
					json['group1']=rank_details.level
					count_flag=1
				else:
					json['group2']=rank_details.level
					count_flag=1

		return render(request,"home/home.html",json)
	else:
		return HttpResponseRedirect('/verify_mobile/')

@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def logout_and_register(request):
	return render(request,"message/message.html",{'message':"Pls Logout and register again"})

def start(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/home")
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	return render(request,'start/start.html',{"login_display":login_display,"login_display2":login_display2})

def contactus(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	return render(request,'contactus/contact_us.html',{"login_display":login_display,"login_display2":login_display2})

def overview(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	return render(request,'overview/overview.html',{"login_display":login_display,"login_display2":login_display2})


def exam_centers(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	return render(request,'exam_center/exam_center.html',{"login_display":login_display,"login_display2":login_display2})

def results(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	#This code is developed by arpit for topper marks
	# try:
	# 	alpha=[]
	# 	exam_group_2=[]
	# 	gamma=[]
	# 	name_2=[]
	# 	name_1=[]
	# 	school_2=[]
	# 	exam_group_1=[]
	# 	school_1=[]
	# 	for o in topper_data.objects.filter(group='alpha'):
	# 		alpha.append(str(o.reference_id))
	# 		user_data_row=user_data.objects.get(refrence_id=o.reference_id)
	# 		print user_data_row.exam_group_2
	# 		exam_group_2.append(str(user_data_row.exam_group_2))
	# 		school_2.append(str(user_data_row.school))
	# 		tem=str(user_data_row.first_name)
	# 		name_2.append(str(tem+" "+user_data_row.last_name))
	# 	for o in topper_data.objects.filter(group='gamma'):
	# 		gamma.append(str(o.reference_id))
	# 		user_data_row=user_data.objects.get(refrence_id=o.reference_id)
	# 		exam_group_1.append(str(user_data_row.exam_group_1))
	# 		school_1.append(str(user_data_row.school))
	# 		tem=str(user_data_row.first_name)
	# 		name_1.append(str(tem+" "+user_data_row.last_name))
	result_data=' '
	result_data1=' '	

	try:
		center_list=topper_data.objects.order_by().values_list('center').distinct()
		group_list=topper_data.objects.order_by().values_list('group').distinct()
		round_list=topper_data.objects.order_by().values_list('current_round').distinct()

		for round_data in round_list:
			print round_data[0]
			for center in center_list:
				print center[0]
				for group in topper_data.objects.filter(center=center[0]).order_by().values_list('group').distinct():
					result_data+='<div class="row"><div class="col s12 m2 "></div><div class="col s12 m8"><div class="card white black-text" background-color="#FFD700"><div class="card-content blue-text"><span class="card-title">'
					result_data+='Topper List '
					result_data+=str(round_data[0])+' '
					result_data+=str(center[0])+' '
					result_data+=str(group[0])+' '
					result_data+='</span><ul class="collection with-header">'
					result_data+='<div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Name">Name</th><th id="th" data-field="Awards">Awards</th></tr></thead>'
					result_data+='<tbody id="'+str(group[0])+'">'
					print group[0]
					for topper_details in topper_data.objects.filter(center=center[0],group=group[0],current_round=round_data[0]).order_by('rank'):
						try:
							user_details=user_data.objects.get(refrence_id=str(topper_details.reference_id))
							name=str(user_details.first_name)+' '+str(user_details.last_name)
						except Exception,e:
							name='Name Not Available'
							print e
						# try:
						# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
						# 	user_details=user_data.objects.get(refrence_id=str(topper_details.reference_id))
						# 	url+=str(user_details.number)
						# 	url+='&message=Congratulations '+ str(user_details.first_name)+ ' ,You are Center Topper for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' and your Center Rank is  '+str(topper_details.rank)+' You will be awarded with '+topper_details.medal+'               Thanks , Team Navmo'
						# 	url+='&sender=mNavmo&route=4'
						# 	print requests.request('GET', url)

						# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
						# 	user_details=user_data.objects.get(refrence_id=str(topper_details.reference_id))
						# 	url+=str('8446019312')
						# 	url+='&message=Congratulations '+ str(user_details.first_name)+ ' ,You are Center Topper for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' and your Center Rank is  '+str(topper_details.rank)+' You will be awarded with '+topper_details.medal+'               Thanks , Team Navmo'
						# 	url+='&sender=mNavmo&route=4'
						# 	print requests.request('GET', url)

						# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
						# 	user_details=user_data.objects.get(refrence_id=str(topper_details.reference_id))
						# 	url+=str('8109109457')
						# 	url+='&message=Congratulations '+ str(user_details.first_name)+ ' ,You are Center Topper for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' and your Center Rank is  '+str(topper_details.rank)+' You will be awarded with '+topper_details.medal+'               Thanks , Team Navmo'
						# 	url+='&sender=mNavmo&route=4'
						# 	print requests.request('GET', url)
						# except Exception,e:
						# 	print e
						
						result_data+='<tr><td id="td">'+str(topper_details.rank)+'</td>'
						result_data+='<td id="td">'+str(topper_details.reference_id)+'</td>'
						result_data+='<td id="td">'+name+'</td>'
						result_data+='<td id="td">'+str(topper_details.medal)+'</td></tr>'
						print topper_details.reference_id
					result_data+='</tbody></table></div></ul></div></div></div></div>'

		for o in results_data.objects.filter():
			result_data1+='<li class=collection-item> Roll Number - '+o.reference_id+'</li>'
			# print o,o.reference_id
			# print result_data1
		return render(request,'results/results.html',{"result_data":result_data,"result_data1":result_data1,"login_display":login_display,"login_display2":login_display2})

		# return render(request,'results/results.html',{"result_data2":result_data,"result_data1"=result_data1,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/results.html',{"result_data":result_data,"result_data1":result_data1,"login_display":login_display,"login_display2":login_display2})
		
		# return render(request,'results/results.html',{"result_data2":result_data,"result_data1"=result_data1,"login_display":login_display,"login_display2":login_display2})

def admin_results(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	
	center_list=marks_data.objects.order_by().values_list('center').distinct()
	group_list=marks_data.objects.order_by().values_list('group').distinct()
	level_list=marks_data.objects.order_by().values_list('level').distinct()
	
	# for center in center_list:
	# 	print center[0]
	# 	for group in marks_data.objects.filter(center=center[0]).order_by().values_list('group').distinct():
	# 		print group[0]
	# 		for level in marks_data.objects.filter(center=center[0],group=group[0]).order_by().values_list('level').distinct():
	# 			print level[0]
	# 			marks_data_list=marks_data.objects.filter(level=level[0])
	# 			topper_marks_first=marks_data_list.aggregate(Max('marks_first'))
	# 			topper_marks_semi=marks_data_list.aggregate(Max('marks_semi'))
	# 			topper_marks_final=marks_data_list.aggregate(Max('marks_final'))
				
	# 			print topper_marks_first
	# 			print topper_marks_semi
	# 			print topper_marks_final


	# 			topper_marks_first= topper_marks_first['marks_first__max']
	# 			topper_marks_semi= topper_marks_semi['marks_semi__max']
	# 			topper_marks_final= topper_marks_final['marks_final__max']

	# 			print topper_marks_first
	# 			print topper_marks_semi
	# 			print topper_marks_final

	# 			for marks_details in marks_data_list:
			
	# 				if topper_marks_final!=0.0 and marks_details.marks_final!=0.0:
	# 					try:
	# 						temp=marks_details.marks_semi/topper_marks_semi
	# 						minutes=int(marks_details.time_semi)
	# 						seconds=marks_details.time_semi-minutes
	# 						time=(minutes*60)+(seconds*100)
	# 						time=time/60
	# 						temp=temp/time# marks_details.npi_semi=temp
	# 						temp=temp*250

	# 						if(group[0]=='alpha'):
	# 							temp=temp*2
	# 						elif(group[0]=='thetha'):
	# 							temp=temp*4							
	# 						setattr(marks_details,'npi_semi',"%.2f" % temp)
	# 						marks_details.save()
	# 					except Exception,e:
	# 						print e
	# 					print 'Final Round'


	# 				if topper_marks_semi!=0.0 and marks_details.marks_semi!=0.0:
	# 					try:
	# 						temp1=marks_details.marks_semi/topper_marks_semi
	# 						minutes=int(marks_details.time_semi)
	# 						seconds=marks_details.time_semi-minutes
	# 						time=(minutes*60)+(seconds*100)
	# 						time=time/60
	# 						temp1=temp1/time# marks_details.npi_semi=temp1
	# 						temp1=temp1*250

	# 						if(group[0]=='alpha'):
	# 							temp1=temp1*2
	# 						elif(group[0]=='thetha'):
	# 							temp1=temp1*4							
	# 						setattr(marks_details,'npi_semi',"%.2f" % temp1)
	# 						marks_details.save()
	# 					except Exception,e:
	# 						print e
	# 					print 'SemiFinal Round'
						
	# 				elif topper_marks_first!=0.0 and marks_details.marks_first!=0.0:
	# 					try:
	# 						temp2=marks_details.marks_first/topper_marks_first
	# 						minutes=int(marks_details.time_first)
	# 						seconds=marks_details.time_first-minutes
	# 						time=(minutes*60)+(seconds*100)
	# 						time=time/60
	# 						temp2=temp2/time# marks_details.npi_first=temp2
	# 						temp2=temp2*250
							
	# 						if(group[0]=='alpha'):
	# 							temp2=temp2*2
	# 						elif(group[0]=='thetha'):
	# 							temp2=temp2*4

	# 						setattr(marks_details,'npi_first',"%.2f" % temp2)
	# 						marks_details.save()

	# 					except Exception,e:
	# 						print e
	# 					print 'First Round'
	result_data=''
	for center in center_list:
		# result_data+='<div class="row"><div class="col s12 m2"></div><div class="col s12 m8"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text">'
		# result_data+='<ul class="collection with-header"><center>'
		# result_data+='<li class="collection-header"><h4>Rank List'+str(center[0])+'</h4></li></center></div></div></div></div>'
		# print center[0]
		for group in marks_data.objects.filter(center=center[0]).order_by().values_list('group').distinct():
			count=1
			result_data+='<div class="row"><div class="col s12 m0 "></div><div class="col s12 m12"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
			result_data+='Rank List '
			result_data+=str(center[0])+' '
			result_data+=str(group[0])+' '
			result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Id">Group-Level</th><th id="th" data-field="Id">NPI Score</th><th id="th" data-field="Id">Current Round</th><th id="th" data-field="Id">National Level Rank</th><th id="th" data-field="Id">National Group Rank</th><th id="th" data-field="Id">Name</th><th id="th" data-field="Id">Father</th><th id="th" data-field="Id">Email</th><th id="th" data-field="Id">School</th><th id="th" data-field="Id">Class</th><th id="th" data-field="Id">Awards</th></tr></thead>'
			result_data+='<tbody id="'+str(group[0])+'">'
			print group[0]
			# for groups_data in marks_data.objects.filter(center=center[0],group=group[0],current_round='Finals' | current_round='').order_by('-npi_semi'):
			# 	# try:
			# # 	# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# # 	# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# # 	# 	url+=str(user_details.number)
			# # 	# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_final)+'.             Thanks , Team Navmo'
			# # 	# 	url+='&sender=mNavmo&route=4'
			# # 	# 	print requests.request('GET', url)
			# # 	# except Exception,e:
			# # 	# 	print e
			# # 	# result_data+='<tr><td id="td">'+str(count)+'</td>'
			# # 	result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			# # 	result_data+='<td id="td">'+str(groups_data.npi_final)+'</td></tr>'
			# 	result_data+='<tr><td id="td">'+str(count)+'</td>'
			# 	result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			# 	result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			# 	result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
			# 	result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
			# 	result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td></tr>'

			# 	count+=1
			# 	print groups_data.reference_id
			for groups_data in marks_data.objects.filter(Q(current_round='Finals') | Q(current_round='Semi-Finals') ,center=center[0],group=group[0]).order_by('-npi_semi'):
				# try:
				# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
				# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
				# 	url+=str(user_details.number)
				# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_semi)+'.%0A%0AThanks , Team Navmo'
				# 	url+='&sender=mNavmo&route=4'
				# 	print requests.request('GET', url)
				# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
				# 	url+=str('8109109457')
				# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_semi)+'.%0A%0AThanks , Team Navmo'
				# 	url+='&sender=mNavmo&route=4'
				# 	print requests.request('GET', url)
				# except Exception,e:
				# 	print e

				result_data+='<tr><td id="td">'+str(count)+'</td>'
				result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
				result_data+='<td id="td">'+str(groups_data.level)+'</td>'
				# result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
				# result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
				result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td>'
				result_data+='<td id="td">'+str(groups_data.current_round)+'</td>'

				try:
					rank_details=rank_data.objects.get(reference_id=groups_data.reference_id ,level=groups_data.level)
					result_data+='<td id="td">'+str(rank_details.national_level_rank)+'</td>'
					result_data+='<td id="td">'+str(rank_details.national_group_rank)+'</td>'
				except Exception,e:
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
					print e
				try:
					user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
					result_data+='<td id="td">'+str(user_details.first_name+" "+user_details.last_name)+'</td>'
					result_data+='<td id="td">'+str(user_details.parent_father)+'</td>'
					result_data+='<td id="td">'+str(user_details.email)+'</td>'
					result_data+='<td id="td">'+str(user_details.school)+'</td>'
					result_data+='<td id="td">'+str(user_details.grade)+'</td>'

				except Exception,e:
					print str(e)
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'

				try:
					award_name=""
					rank_details=rank_data.objects.get(reference_id=groups_data.reference_id ,level=groups_data.level)
					if groups_data.current_round=="Finals":
						if rank_details.national_level_rank==1:
							award_name="National Gold Medal + Champion's Champion Trophy"
						elif rank_details.national_level_rank==2:
							award_name="National Silver Medal + National Champion Trophy"
						elif rank_details.national_level_rank==3:
							award_name="National Bronze Medal + National Champion Trophy"
						else:
							award_name="National Champion Trophy"
					if groups_data.current_round=="Finals":
						if count==1:
							award_name+=" + School Gold Medal"
						elif count==2:
							award_name+=" + School Silver Medal"
						elif count==3:
							award_name+=" + School Bronze Medal"
					else:
						if count==1:
							award_name+="School Gold Medal"
						elif count==2:
							award_name+="School Silver Medal"
						elif count==3:
							award_name+="School Bronze Medal"
					result_data+='<td id="td">'+award_name+'</td></tr>'
				except Exception,e:
					print e
				# rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
				# rank_details.centre_rank=count
				# rank_details.save()
				count+=1

				print groups_data.reference_id
			for groups_data in marks_data.objects.filter(center=center[0],group=group[0],current_round='First-Round').order_by('-npi_first'):
				# try:
				# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
				# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
				# 	url+=str(user_details.number)
				# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_first)+'.%0A%0AThanks , Team Navmo'
				# 	url+='&sender=mNavmo&route=4'
				# 	print requests.request('GET', url)
				# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
				# 	url+=str('8109109457')
				# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_first)+'.%0A%0AThanks , Team Navmo'
				# 	url+='&sender=mNavmo&route=4'
				# 	print requests.request('GET', url)
				# except Exception,e:
				# 	print e

				result_data+='<tr><td id="td">'+str(count)+'</td>'
				result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
				result_data+='<td id="td">'+str(groups_data.level)+'</td>'
				# result_data+='<td id="td">'+str(groups_data.marks_first)+'</td>'
				# result_data+='<td id="td">'+str(groups_data.time_first)+'</td>'
				result_data+='<td id="td">'+str(groups_data.npi_first)+'</td>'
				result_data+='<td id="td">'+str(groups_data.current_round)+'</td>'

				try:
					rank_details=rank_data.objects.get(reference_id=groups_data.reference_id ,level=groups_data.level)
					result_data+='<td id="td">'+str(rank_details.national_level_rank)+'</td>'
					result_data+='<td id="td">'+str(rank_details.national_group_rank)+'</td>'
				except Exception,e:
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
					print e
			
				try:
					user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
					result_data+='<td id="td">'+str(user_details.first_name+" "+user_details.last_name)+'</td>'
					result_data+='<td id="td">'+str(user_details.parent_father)+'</td>'
					result_data+='<td id="td">'+str(user_details.email)+'</td>'
					result_data+='<td id="td">'+str(user_details.school)+'</td>'
					result_data+='<td id="td">'+str(user_details.grade)+'</td>'

				except Exception,e:
					print str(e)
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
					result_data+='<td id="td">'+"N A"+'</td>'
				try:
					award_name=""
					rank_details=rank_data.objects.get(reference_id=groups_data.reference_id ,level=groups_data.level)
					if groups_data.current_round=="Finals":
						if rank_details.national_level_rank==1:
							award_name="National Gold Medal + Champion's Champion Trophy"
						elif rank_details.national_level_rank==2:
							award_name="National Silver Medal + National Champion Trophy"
						elif rank_details.national_level_rank==3:
							award_name="National Bronze Medal + National Champion Trophy"
						else :
							award_name="National Champion Trophy"
					if groups_data.current_round=="Finals":
						if rank_details.centre_rank==1:
							award_name+=" + School Gold Medal"
						elif rank_details.centre_rank==2:
							award_name+=" + School Silver Medal"
						elif rank_details.centre_rank==3:
							award_name+=" + School Bronze Medal"
					else:
						if rank_details.centre_rank==1:
							award_name+="School Gold Medal"
						elif rank_details.centre_rank==2:
							award_name+="School Silver Medal"
						elif rank_details.centre_rank==3:
							award_name+="School Bronze Medal"
					
					result_data+='<td id="td">'+award_name+'</td></tr>'
				except Exception,e:
					print e
				# rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
				# rank_details.centre_rank=count
				# rank_details.save()
				count+=1

				print groups_data.reference_id

			result_data+='</tbody></table></div></ul></div></div></div></div>'
	try:
		return render(request,'results/admin_results.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/admin_results.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})



def admin_results1(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	
	center_list=marks_data.objects.order_by().values_list('center').distinct()
	group_list=marks_data.objects.order_by().values_list('group').distinct()
	level_list=marks_data.objects.order_by().values_list('level').distinct()
	
	for center in center_list:
		print center[0]
		for group in marks_data.objects.filter(center=center[0]).order_by().values_list('group').distinct():
			print group[0]
			for level in marks_data.objects.filter(center=center[0],group=group[0]).order_by().values_list('level').distinct():
				print level[0]
				marks_data_list=marks_data.objects.filter(level=level[0])
				topper_marks_first=marks_data_list.aggregate(Max('marks_first'))
				topper_marks_semi=marks_data_list.aggregate(Max('marks_semi'))
				topper_marks_final=marks_data_list.aggregate(Max('marks_final'))
				
				print topper_marks_first
				print topper_marks_semi
				print topper_marks_final


				topper_marks_first= topper_marks_first['marks_first__max']
				topper_marks_semi= topper_marks_semi['marks_semi__max']
				topper_marks_final= topper_marks_final['marks_final__max']

				print topper_marks_first
				print topper_marks_semi
				print topper_marks_final

				for marks_details in marks_data_list:
					# if topper_marks_final!=0.0 and marks_details.marks_final!=0.0:
					# 	try:
					# 		temp=marks_details.marks_final/topper_marks_final
					# 		minutes=int(marks_details.time_final)
					# 		seconds=marks_details.time_final-minutes
					# 		time=(minutes*60)+(seconds*100)
					# 		time=time/60
					# 		temp=temp/time
					# 		temp=temp*250
					# 		if(group[0]=='alpha'):
					# 			temp=temp*2
					# 		elif(group[0]=='thetha'):
					# 			temp=temp*4	

					# 		print marks_details.time_final
					# 		print minutes
					# 		print seconds
					# 		print time
					# 		# marks_details.npi_final=temp
					# 		setattr(marks_details,'npi_final',"%.2f" % temp)
					# 		marks_details.save()
					# 	except Exception,e:
					# 		print e
					# 	print 'Final Round'

					if topper_marks_semi!=0.0 and marks_details.marks_semi!=0.0:
						try:
							temp1=marks_details.marks_semi/topper_marks_semi
							minutes=int(marks_details.time_semi)
							seconds=marks_details.time_semi-minutes
							time=(minutes*60)+(seconds*100)
							time=time/60
							temp1=temp1/time# marks_details.npi_semi=temp1
							temp1=temp1*250

							if(group[0]=='alpha'):
								temp1=temp1*2
							elif(group[0]=='thetha'):
								temp1=temp1*4							
							setattr(marks_details,'npi_semi',"%.2f" % temp1)
							marks_details.save()
						except Exception,e:
							print e
						print 'SemiFinal Round'
						
					elif topper_marks_first!=0.0 and marks_details.marks_first!=0.0:
						try:
							temp2=marks_details.marks_first/topper_marks_first
							minutes=int(marks_details.time_first)
							seconds=marks_details.time_first-minutes
							time=(minutes*60)+(seconds*100)
							time=time/60
							temp2=temp2/time# marks_details.npi_first=temp2
							temp2=temp2*250
							
							if(group[0]=='alpha'):
								temp2=temp2*2
							elif(group[0]=='thetha'):
								temp2=temp2*4

							setattr(marks_details,'npi_first',"%.2f" % temp2)
							marks_details.save()

						except Exception,e:
							print e
						print 'First Round'
	result_data=''
	 # for level in level_list:
		# result_data+='<div class="row"><div class="col s12 m2"></div><div class="col s12 m8"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text">'
		# result_data+='<ul class="collection with-header"><center>'
		# result_data+='<li class="collection-header"><h4>Rank List'+str(center[0])+'</h4></li></center></div></div></div></div>'
		# print center[0]
	for level in level_list:
		count=1
		result_data+='<div class="row"><div class="col s12 m0 "></div><div class="col s12 m12"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
		result_data+='Rank List '
		result_data+=str(level[0])+' '
		result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Id">Group-Level</th><th id="th" data-field="Id">Marks</th><th id="th" data-field="Id">Time</th><th id="th" data-field="Id">NPI Score</th></tr></thead>'
		result_data+='<tbody id="'+str(level[0])+'">'
		print group[0]
		# for groups_data in marks_data.objects.filter(level=level[0],current_round='Finals').order_by('-npi_final'):
		# 	# try:
		# 	# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
		# 	# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
		# 	# 	url+=str(user_details.number)
		# 	# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_final)+'.             Thanks , Team Navmo'
		# 	# 	url+='&sender=mNavmo&route=4'
		# 	# 	print requests.request('GET', url)
		# 	# except Exception,e:
		# 	# 	print e
		# 	# result_data+='<tr><td id="td">'+str(count)+'</td>'
		# 	result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
		# 	result_data+='<td id="td">'+str(groups_data.npi_final)+'</td></tr>'
		# 	count+=1
		# 	print groups_data.reference_id
		for groups_data in marks_data.objects.filter(level=level[0],current_round='Semi-Finals').order_by('-npi_semi'):
			# try:
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# 	url+=str(user_details.number)
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_semi)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	url+=str('8109109457')
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_semi)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# except Exception,e:
			# 	print e
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
			result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
			result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td></tr>'
			count+=1
			print groups_data.reference_id
		for groups_data in marks_data.objects.filter(level=level[0],current_round='First-Round').order_by('-npi_first'):
			# try:
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# 	url+=str(user_details.number)
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_first)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	url+=str('9049019312')
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_first)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# except Exception,e:
			# 	print e
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			result_data+='<td id="td">'+str(groups_data.marks_first)+'</td>'
			result_data+='<td id="td">'+str(groups_data.time_first)+'</td>'
			result_data+='<td id="td">'+str(groups_data.npi_first)+'</td></tr>'
			count+=1
			print groups_data.reference_id
		result_data+='</tbody></table></div></ul></div></div></div></div>'
	try:
		return render(request,'results/admin_results.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/admin_results.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})



def admin_final_result_groupwise(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	
	# center_list=marks_data.objects.order_by().values_list('center').distinct()
	group_list=marks_data.objects.order_by().values_list('group').distinct()
	level_list=marks_data.objects.order_by().values_list('level').distinct()
	

	for group in marks_data.objects.filter().order_by().values_list('group').distinct():
		print group[0]
		for level in marks_data.objects.filter(group=group[0]).order_by().values_list('level').distinct():
			print level[0]
			marks_data_list=marks_data.objects.filter(level=level[0])
			topper_marks_first=marks_data_list.aggregate(Max('marks_first'))
			topper_marks_semi=marks_data_list.aggregate(Max('marks_semi'))
			topper_marks_final=marks_data_list.aggregate(Max('marks_final'))				
			print topper_marks_first
			print topper_marks_semi
			print topper_marks_final
			topper_marks_first= topper_marks_first['marks_first__max']
			topper_marks_semi= topper_marks_semi['marks_semi__max']
			topper_marks_final= topper_marks_final['marks_final__max']
			print topper_marks_first
			print topper_marks_semi
			print topper_marks_final
			for marks_details in marks_data_list:
				if topper_marks_final!=0.0 and marks_details.marks_final!=0.0:
					try:
						temp=marks_details.marks_final/topper_marks_final
						minutes=int(marks_details.time_final)
						seconds=marks_details.time_final-minutes
						time=(minutes*60)+(seconds*100)
						time=time/60
						temp=temp/time
						temp=temp*250
						if(group[0]=='alpha'):
							temp=temp*2
						elif(group[0]=='thetha'):
							temp=temp*4	
						print marks_details.time_final
						print minutes
						print seconds
						print time
						# marks_details.npi_final=temp
						setattr(marks_details,'npi_final',"%.2f" % temp)
						marks_details.save()
					except Exception,e:
						print e

	result_data=''
	for group in marks_data.objects.filter(current_round="Finals").order_by().values_list('group').distinct():
		count=1
		result_data+='<div class="row"><div class="col s12 m2 "></div><div class="col s12 m8"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
		result_data+='Rank List '
		result_data+=str(group[0])+' '
		result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Id">Name</th><th id="th" data-field="Id">Center</th><th id="th" data-field="Id">Group-Level</th><th id="th" data-field="Id">Marks</th><th id="th" data-field="Id">Time</th><th id="th" data-field="Id">NPI Score</th></tr></thead>'
		result_data+='<tbody id="'+str(group[0])+'">'
		print group[0]
		for groups_data in marks_data.objects.filter(group=group[0],current_round='Finals').order_by('-npi_final'):
			# try:
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# 	url+=str(user_details.number)
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_final)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# except Exception,e:
			# 	print e
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			try:
				user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
				result_data+='<td id="td">'+str(user_details.first_name+' '+user_details.last_name)+'</td>'
			except Exception,e:
				print e
				result_data+='<td id="td">'+str(' ')+'</td>'

			result_data+='<td id="td">'+str(groups_data.center)+'</td>'
			result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			result_data+='<td id="td">'+str(groups_data.marks_final)+'</td>'
			result_data+='<td id="td">'+str(groups_data.time_final)+'</td>'
			result_data+='<td id="td">'+str(groups_data.npi_final)+'</td></tr>'
		
			count+=1
			print groups_data.reference_id
		
			
		result_data+='</tbody></table></div></ul></div></div></div></div>'
	try:
		return render(request,'results/admin_results.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/admin_results.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})



def admin_final_result_levelwise(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	
	center_list=marks_data.objects.order_by().values_list('center').distinct()
	group_list=marks_data.objects.order_by().values_list('group').distinct()
	level_list=marks_data.objects.order_by().values_list('level').distinct()
	
	
	for group in marks_data.objects.filter().order_by().values_list('group').distinct():
		print group[0]
		for level in marks_data.objects.filter(group=group[0]).order_by().values_list('level').distinct():
			print level[0]
			marks_data_list=marks_data.objects.filter(level=level[0])
			topper_marks_first=marks_data_list.aggregate(Max('marks_first'))
			topper_marks_semi=marks_data_list.aggregate(Max('marks_semi'))
			topper_marks_final=marks_data_list.aggregate(Max('marks_final'))			
			print topper_marks_first
			print topper_marks_semi
			print topper_marks_final
			topper_marks_first= topper_marks_first['marks_first__max']
			topper_marks_semi= topper_marks_semi['marks_semi__max']
			topper_marks_final= topper_marks_final['marks_final__max']
			print topper_marks_first
			print topper_marks_semi
			print topper_marks_final
			for marks_details in marks_data_list:
				if topper_marks_final!=0.0 and marks_details.marks_final!=0.0:
					try:
						temp=marks_details.marks_final/topper_marks_final
						minutes=int(marks_details.time_final)
						seconds=marks_details.time_final-minutes
						time=(minutes*60)+(seconds*100)
						time=time/60
						temp=temp/time
						temp=temp*250
						if(group[0]=='alpha'):
							temp=temp*2
						elif(group[0]=='thetha'):
							temp=temp*4	
						print marks_details.time_final
						print minutes
						print seconds
						print time
						# marks_details.npi_final=temp
						setattr(marks_details,'npi_final',"%.2f" % temp)
						marks_details.save()
					except Exception,e:
						print e
					print 'Final Round'
	result_data=''
	 # for level in level_list:
		# result_data+='<div class="row"><div class="col s12 m2"></div><div class="col s12 m8"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text">'
		# result_data+='<ul class="collection with-header"><center>'
		# result_data+='<li class="collection-header"><h4>Rank List'+str(center[0])+'</h4></li></center></div></div></div></div>'
		# print center[0]
	for level in level_list:
		count=1
		result_data+='<div class="row"><div class="col s12 m0 "></div><div class="col s12 m12"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
		result_data+='Rank List '
		result_data+=str(level[0])+' '
		result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Id">Name</th><th id="th" data-field="Id">Center</th><th id="th" data-field="Id">Group-Level</th><th id="th" data-field="Id">Marks</th><th id="th" data-field="Id">Time</th><th id="th" data-field="Id">NPI Score</th></tr></thead>'
		result_data+='<tbody id="'+str(level[0])+'">'
		print group[0]
		for groups_data in marks_data.objects.filter(level=level[0],current_round='Finals').order_by('-npi_final'):
			# try:
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# 	url+=str(user_details.number)
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_final)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# except Exception,e:
			# 	print e
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
		
			try:
				user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
				result_data+='<td id="td">'+str(user_details.first_name+' '+user_details.last_name)+'</td>'
			except Exception,e:
				print e
				result_data+='<td id="td">'+str(' ')+'</td>'

			result_data+='<td id="td">'+str(groups_data.center)+'</td>'


			result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			result_data+='<td id="td">'+str(groups_data.marks_final)+'</td>'
			result_data+='<td id="td">'+str(groups_data.time_final)+'</td>'
			result_data+='<td id="td">'+str(groups_data.npi_final)+'</td></tr>'
			
			count+=1
			print groups_data.reference_id
		
		result_data+='</tbody></table></div></ul></div></div></div></div>'
	try:
		return render(request,'results/admin_results.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/admin_results.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})



def national_result_levelwise(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	
	center_list=marks_data.objects.order_by().values_list('center').distinct()
	group_list=marks_data.objects.order_by().values_list('group').distinct()
	level_list=marks_data.objects.order_by().values_list('level').distinct()
	
	
	for group in marks_data.objects.filter().order_by().values_list('group').distinct():
		print group[0]
		for level in marks_data.objects.filter(group=group[0]).order_by().values_list('level').distinct():
			print level[0]
			marks_data_list=marks_data.objects.filter(level=level[0])
			topper_marks_first=marks_data_list.aggregate(Max('marks_first'))
			topper_marks_semi=marks_data_list.aggregate(Max('marks_semi'))
			topper_marks_final=marks_data_list.aggregate(Max('marks_final'))			
			print topper_marks_first
			print topper_marks_semi
			print topper_marks_final
			topper_marks_first= topper_marks_first['marks_first__max']
			topper_marks_semi= topper_marks_semi['marks_semi__max']
			topper_marks_final= topper_marks_final['marks_final__max']
			print topper_marks_first
			print topper_marks_semi
			print topper_marks_final
			for marks_details in marks_data_list:
				if topper_marks_final!=0.0 and marks_details.marks_final!=0.0:
					try:
						temp=marks_details.marks_final/topper_marks_final
						minutes=int(marks_details.time_final)
						seconds=marks_details.time_final-minutes
						time=(minutes*60)+(seconds*100)
						time=time/60
						temp=temp/time
						temp=temp*250
						if(group[0]=='alpha'):
							temp=temp*2
						elif(group[0]=='thetha'):
							temp=temp*4	
						print marks_details.time_final
						print minutes
						print seconds
						print time
						# marks_details.npi_final=temp
						setattr(marks_details,'npi_final',"%.2f" % temp)
						marks_details.save()
					except Exception,e:
						print e
					print 'Final Round'
	result_data=''
	 # for level in level_list:
		# result_data+='<div class="row"><div class="col s12 m2"></div><div class="col s12 m8"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text">'
		# result_data+='<ul class="collection with-header"><center>'
		# result_data+='<li class="collection-header"><h4>Rank List'+str(center[0])+'</h4></li></center></div></div></div></div>'
		# print center[0]
	for level in level_list.order_by('level'):
		count=1
		result_data+='<div class="row"><div class="col s12 m1 "></div><div class="col s12 m10"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
		result_data+='Rank List '
		result_data+=(str(level[0])).title()+' '
		result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank"><center>Rank</th><th id="th"data-field="Id"><center>Roll Number</th><th id="th" data-field="Id"><center>Name</th><th id="th"data-field="Id"><center>Class</th><th id="th"data-field="Id"><center>NPI Score</th><th id="th"data-field="Id"><center>Awards</th></tr></thead>'
		result_data+='<tbody id="'+str(level[0])+'">'
		print group[0]
		for groups_data in marks_data.objects.filter(level=level[0],current_round='Finals').order_by('-npi_final'):
			# try:
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# 	url+=str(user_details.number)
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_final)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# except Exception,e:
			# 	print e
			if groups_data.npi_final!=0.0:
				result_data+='<tr><td id="td"><center>'+str(count)+'</td>'
				result_data+='<td id="td"><center>'+str(groups_data.reference_id)+'</td>'
			
				try:
					user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
					result_data+='<td id="td" width="20%">'+(str(user_details.first_name+' '+user_details.last_name)).upper()+'</td>'
					result_data+='<td id="td"><center>'+str(user_details.grade)+'</td>'
				except Exception,e:
					print e
					result_data+='<td id="td">'+str(' ')+'</td>'
					result_data+='<td id="td">'+"Not Available"+'</td>'



				#result_data+='<td id="td"<center>'+str(groups_data.level)+'</td>'
				result_data+='<td id="td"><center>'+str(groups_data.npi_final)+'</td>'
				try:
					if count==1:
						award_name="National Gold Medal & Champion's Champion Trophy"
					elif count==2:
						award_name="National Silver Medal & National Champion Trophy"
					elif count==3:
						award_name="National Bronze Medal & National Champion Trophy"
					else:
						award_name="National Champion Trophy"

					result_data+='<td id="td" width="30%">'+award_name+'</td></tr>'
				except Exception,e:
					print e
				
				count+=1
				print groups_data.reference_id

		
		result_data+='</tbody></table></div></ul></div></div></div></div>'
	try:
		return render(request,'results/admin_results.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/admin_results.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})

#----------------------------------------------
def admin_certificate(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	
	print 'meghal'
	center_list=marks_data.objects.order_by().values_list('center').distinct()
	group_list=marks_data.objects.order_by().values_list('group').distinct()
	level_list=marks_data.objects.order_by().values_list('level').distinct()
	
	# for center in center_list:
	# 	print center[0]
	# 	for group in marks_data.objects.filter(center=center[0]).order_by().values_list('group').distinct():
	# 		print group[0]
	# 		for level in marks_data.objects.filter(center=center[0],group=group[0]).order_by().values_list('level').distinct():
	# 			print level[0]
	# 			marks_data_list=marks_data.objects.filter(level=level[0])
	# 			topper_marks_first=marks_data_list.aggregate(Max('marks_first'))
	# 			topper_marks_semi=marks_data_list.aggregate(Max('marks_semi'))
	# 			topper_marks_final=marks_data_list.aggregate(Max('marks_final'))
				
	# 			print topper_marks_first
	# 			print topper_marks_semi
	# 			print topper_marks_final


	# 			topper_marks_first= topper_marks_first['marks_first__max']
	# 			topper_marks_semi= topper_marks_semi['marks_semi__max']
	# 			topper_marks_final= topper_marks_final['marks_final__max']

	# 			print topper_marks_first
	# 			print topper_marks_semi
	# 			print topper_marks_final

	# 			for marks_details in marks_data_list:
	# 				if topper_marks_final!=0.0 and marks_details.marks_final!=0.0:
	# 					try:
	# 						temp=marks_details.marks_final/topper_marks_final
	# 						minutes=int(marks_details.time_final)
	# 						seconds=marks_details.time_final-minutes
	# 						time=(minutes*60)+(seconds*100)
	# 						time=time/60
	# 						temp=temp/time
	# 						temp=temp*250
	# 						if(group[0]=='alpha'):
	# 							temp=temp*2
	# 						elif(group[0]=='thetha'):
	# 							temp=temp*4	

	# 						print marks_details.time_final
	# 						print minutes
	# 						print seconds
	# 						print time
	# 						# marks_details.npi_final=temp
	# 						setattr(marks_details,'npi_final',"%.2f" % temp)
	# 						marks_details.save()
	# 					except Exception,e:
	# 						print e
	# 					print 'Final Round'

	# 				elif topper_marks_semi!=0.0 and marks_details.marks_semi!=0.0:
	# 					try:
	# 						temp1=marks_details.marks_semi/topper_marks_semi
	# 						minutes=int(marks_details.time_semi)
	# 						seconds=marks_details.time_semi-minutes
	# 						time=(minutes*60)+(seconds*100)
	# 						time=time/60
	# 						temp1=temp1/time# marks_details.npi_semi=temp1
	# 						temp1=temp1*250

	# 						if(group[0]=='alpha'):
	# 							temp1=temp1*2
	# 						elif(group[0]=='thetha'):
	# 							temp1=temp1*4							
	# 						setattr(marks_details,'npi_semi',"%.2f" % temp1)
	# 						marks_details.save()
	# 					except Exception,e:
	# 						print e
	# 					print 'SemiFinal Round'
						
	# 				elif topper_marks_first!=0.0 and marks_details.marks_first!=0.0:
	# 					try:
	# 						temp2=marks_details.marks_first/topper_marks_first
	# 						minutes=int(marks_details.time_first)
	# 						seconds=marks_details.time_first-minutes
	# 						time=(minutes*60)+(seconds*100)
	# 						time=time/60
	# 						temp2=temp2/time# marks_details.npi_first=temp2
	# 						temp2=temp2*250
							
	# 						if(group[0]=='alpha'):
	# 							temp2=temp2*2
	# 						elif(group[0]=='thetha'):
	# 							temp2=temp2*4

	# 						setattr(marks_details,'npi_first',"%.2f" % temp2)
	# 						marks_details.save()

	# 					except Exception,e:
	# 						print e
	# 					print 'First Round'
	result_data=''
	 # for level in level_list:
		# result_data+='<div class="row"><div class="col s12 m2"></div><div class="col s12 m8"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text">'
		# result_data+='<ul class="collection with-header"><center>'
		# result_data+='<li class="collection-header"><h4>Rank List'+str(center[0])+'</h4></li></center></div></div></div></div>'
		# print center[0]
	for level in level_list:
		count=1
		result_data+='<div class="row"><div class="col s12 m0 "></div><div class="col s12 m12"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
		result_data+='Rank List '
		result_data+=str(level[0])+' '
		result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Id">First Name</th><th id="th" data-field="Id">Last Name</th><th id="th" data-field="Id">Father Name</th><th id="th" data-field="Id">Grade</th><th id="th" data-field="Id">School</th><th id="th" data-field="Id">Level</th></tr></thead>'
		result_data+='<tbody id="'+str(level[0])+'">'
		# print group[0]
		for groups_data in marks_data.objects.filter(level=level[0],current_round='Finals').order_by('-npi_semi'):
			# try:
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# 	url+=str(user_details.number)
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_final)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# except Exception,e:
			# 	print e
			# result_data+='<tr><td id="td">'+str(count)+'</td>'
			# result_data+='<tr><td id="td">'+str(groups_data.reference_id)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.npi_final)+'</td></tr>'
			# count+=1
			# print groups_data.reference_id
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
			try:
				user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
				result_data+='<td id="td">'+str(user_details.first_name)+'</td>'
				result_data+='<td id="td">'+str(user_details.last_name)+'</td>'
				result_data+='<td id="td">'+str(user_details.parent_father)+'</td>'
				result_data+='<td id="td">'+str(user_details.grade)+'</td>'
				result_data+='<td id="td">'+str(user_details.school)+'</td>'
				
			except Exception,e:
				print e
				result_data+='<td id="td">'+str('')+'</td>'
				result_data+='<td id="td">'+str('')+'</td>'
				result_data+='<td id="td">'+str('')+'</td>'
				result_data+='<td id="td">'+str('')+'</td>'
				result_data+='<td id="td">'+str('')+'</td>'
			result_data+='<td id="td">'+str(groups_data.level)+'</td></tr>'

			# result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td></tr>'
			count+=1
			print groups_data.reference_id
		# for groups_data in marks_data.objects.filter(level=level[0],current_round='Semi-Finals').order_by('-npi_semi'):
			# try:
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# 	url+=str(user_details.number)
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_semi)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	url+=str('8109109457')
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_semi)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# except Exception,e:
			# 	print e
		# 	result_data+='<tr><td id="td">'+str(count)+'</td>'
		# 	result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
		# 	result_data+='<td id="td">'+str(groups_data.level)+'</td>'
		# 	result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
		# 	result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
		# 	result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td></tr>'
		# 	count+=1
		# 	print groups_data.reference_id
		# for groups_data in marks_data.objects.filter(level=level[0],current_round='First-Round').order_by('-npi_first'):
			# try:
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
			# 	url+=str(user_details.number)
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_first)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# 	url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='
			# 	url+=str('9049019312')
			# 	url+='&message=Dear '+ str(user_details.first_name)+ ' , Tentative Group Wise Center Rank for '+str(group[0])+' group NAVMO 2016 for Reference Id '+str(user_details.refrence_id)+' is '+str(count)+' and NPI Score ( NAVMO Percentile Score) is '+str(groups_data.npi_first)+'.             Thanks , Team Navmo'
			# 	url+='&sender=mNavmo&route=4'
			# 	print requests.request('GET', url)
			# except Exception,e:
			# 	print e
			# result_data+='<tr><td id="td">'+str(count)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.marks_first)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.time_first)+'</td>'
			# result_data+='<td id="td">'+str(groups_data.npi_first)+'</td></tr>'
			# count+=1
			# print groups_data.reference_id
		result_data+='</tbody></table></div></ul></div></div></div></div>'
	try:
		return render(request,'results/admin_results.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/admin_results.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})



	
def syllabus(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	return render(request,'syllabus/syllabus.html',{"login_display":login_display,"login_display2":login_display2})	


def faqs(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	return render(request,'faqs/faqs.html',{"login_display":login_display,"login_display2":login_display2})

def message(request):
	message=request.session['message']
	return render(request,'message/message.html',{'message':message})

def send_message(request):
	response_data={}
	try:
		user_details_list=user_data.objects.all()
		for o in user_details_list:
			url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='			
			url+=str(o.number)
			url+='&message=Mind Power Education Wishes you a Very Happy New Year 2017.%0A%0AMay each day of the coming year be Vibrant and New Bringing along Many reasons for Celebrations and Rejoices.%0A%0ATeam Navmo'
			url+='&sender=MpeEdu&route=4'
			print url
			print requests.request('GET', url)
		url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='			
		url+=str(8446019312)
		url+='&message=Mind Power Education Wishes you a Very Happy New Year 2017.%0A%0AMay each day of the coming year be Vibrant and New Bringing along many reasons for Celebrations and Rejoices.%0A%0ATeam Navmo'
		url+='&sender=MpeEdu&route=4'
		print url
		print requests.request('GET', url)


		url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='			
		url+=str(8109109457)
		url+='&message=Mind Power Education Wishes you a Very Happy New Year 2017.%0A%0AMay each day of the coming year be Vibrant and New Bringing along many reasons for Celebrations and Rejoices.%0A%0ATeam Navmo'
		url+='&sender=MpeEdu&route=4'
		print url
		print requests.request('GET', url)

		url='http://api.msg91.com/api/sendhttp.php?authkey=125195AvX4LUlVf57dcd941&mobiles='			
		url+=str(9907890199)
		url+='&message=Mind Power Education Wishes you a Very Happy New Year 2017.%0A%0AMay each day of the coming year be Vibrant and New Bringing along many reasons for Celebrations and Rejoices.%0A%0ATeam Navmo'
		url+='&sender=MpeEdu&route=4'
		print url
		print requests.request('GET', url)
			
		response_data['success']=True
		response_data['message']="Sent Successfully"
	except Exception,e:
		print e
		response_data['success']=False
		response_data['message']="Error"+e
	return JsonResponse(response_data)


def upgrade_marks_data(request):
	try:
		count=1
		marks_list=marks_data.objects.filter(current_round="Finals")
		for o in marks_list:	
			print count
			print o
			count+=1
	except Exception,e:
		print e,o['ref_id']
	# print 'Group'
	# response = requests.post('http://mpenavmo.com:8080/register810/', data=o)
	# content = response.content
	# print content
	return JsonResponse({})

def upload_final_result(request):
	with open('marks_list.json') as data_file:
		data = json.load(data_file)
		print data
	for o in data:
		try:
			print 'marks',o['marks']
			print 'marks',o['time']
			print 'group',o['group']
			marks_details=marks_data.objects.get(reference_id=o['refrence_id'],group=o['group'])
			marks_details.marks_final=float(o['marks'])
			marks_details.time_final=float(o['time'])
			marks_details.save()
			print 'Done for Reference id - '+str(o['refrence_id'])
		except Exception,e:
			print e
	return JsonResponse({})