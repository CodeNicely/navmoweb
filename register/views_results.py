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
from django.contrib.auth import authenticate
from otp.models import otp_data
from payment.models import payment_data
import random
from .models import exam_center_data
from .models import results_data
from django.core.urlresolvers import reverse
import requests
from django.core.mail import send_mail
from admit_card.models import *
import json
from django.db.models import Q
from .models import rank_data
from random import randint
from django.template.loader import get_template 
from django.template import Context
import pdfkit
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage
import os
from datetime import datetime,timedelta
import threading
from threading import Timer
import sched, time,subprocess
from subprocess import Popen, PIPE, STDOUT
import smtplib
from email.mime.text import MIMEText
import sys
import zipfile,cStringIO,StringIO

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def mail_spr_for_id(request):
	filename=""
	json={}
	json['BASE_DIR']=BASE_DIR
	url_path=str(request.scheme+"://"+request.get_host())
	get_ref_id=request.GET.get('refid')
	json['url_path']=url_path
	count=0;
	try :
		for rank_details in rank_data.objects.filter(reference_id=get_ref_id):
			try:
				filename="navmo_spr_"+rank_details.reference_id+"_"+rank_details.level+".pdf"
				print rank_details.reference_id
				user_details=user_data.objects.get(refrence_id=rank_details.reference_id)
				try:
					image_name=str(user_details.image).replace(" ","%20")
					path=url_path+"/media/"+image_name
					json['image']=path
					if "media" in image_name and "default" not in image_name:
						path=url_path+image_name
						json['image']=path
					if str(user_details.image)==(str(user_details.refrence_id)+"/image") or str(user_details.image)=="/media/default.png":
						path=url_path+"/media/icon.png"
						json['image']=path
					print "Image Path = ",path
				except Exception,e:
					print "Exception on image :",e
					path=url_path+"/media/"+"icon.png"
					json['image']=path
				json['reference_id']=rank_details.reference_id
				json['name']=(str(user_details.first_name+' '+user_details.last_name)).title()
				if (user_details.last_name).lower() in (user_details.parent_father).lower():
					father=(user_details.parent_father).title()
				else:
					father=(user_details.parent_father+" "+user_details.last_name).title()
				json['father']=father
				json['class']=(str(user_details.grade)).title()
				school=""
				if "icis" in (user_details.school).lower() or "cadet" in (user_details.school).lower():
					school="Intelligent Cadet International School"
				elif "goel" in (user_details.school).lower() or "n h" in (user_details.school).lower() or "nh" in (user_details.school).lower() or "n.h." in (user_details.school).lower():
					school="N H Goel World School"
				elif "birla" in (user_details.school).lower():
					school="B K Birla Centre For Education"
				elif "atelier" in (user_details.school).lower():
					school="Atelier International Preschool"
				elif "vibgyor" in (user_details.school).lower():
					school="Vibgyor High School"
				elif "tree" in (user_details.school).lower() or "house" in (user_details.school).lower():
					school="Tree House High School"
				elif "gumla" in (user_details.school).lower():
					school="D.A.V.Public School"
				elif "podar" in (user_details.school).lower():
					school="Podar International School"
				elif "dps" in (user_details.school).lower():
					school="Delhi Public School"
				else:
					school=str(user_details.school).title()
				json['school']=school
			except Exception,e:
				print e
				json['name']="Not Available"
				json['father']="Not Available"
				json['class']="Not Available"
				json['school']="Not Available"
			json['level']=(rank_details.level).title()
			marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
			json['round']=marks_details.current_round
			if marks_details.current_round=='Finals':
				if marks_details.npi_final!=0:
					json['round']=marks_details.current_round
					json['marks']=marks_details.marks_final
					json['time']=marks_details.time_final
					json['npi']=marks_details.npi_final
				else:
					json['round']="Semi-Finals"
					json['marks']=marks_details.marks_semi
					json['time']=marks_details.time_semi
					json['npi']=marks_details.npi_semi
			elif marks_details.current_round=='Semi-Finals':
				json['round']=marks_details.current_round
				json['marks']=marks_details.marks_semi
				json['time']=marks_details.time_semi
				json['npi']=marks_details.npi_semi
			elif marks_details.current_round=='First-Round':
				json['round']=marks_details.current_round
				json['marks']=marks_details.marks_first
				json['time']=marks_details.time_first
				json['npi']=marks_details.npi_first		

			marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
			json['centre_rank']=rank_details.centre_rank
			json['national_level_rank']=rank_details.national_level_rank
			json['national_group_rank']=rank_details.national_group_rank
			try:
				#===================send html to PDF form =======================
				options = {
				# 'page-width':'656.166667',
				# 'page-height':'928.158333',
				'margin-left':'0',
				'margin-right':'0',
				'margin-top':'0',
				'margin-bottom':'0'}
				template=get_template("spr_report/spr_a4.html")
				context = Context(json)  # data is the context data that is sent to the html file to render the output. 
				html = template.render(context)  # Renders the template with the context data.
				pdf=pdfkit.from_string(html, False,options=options)
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename=filename'
				data={}
				data['msg']="Group = "+marks_details.group
				data['msg_head']="Centre = "+marks_details.center
				subject_mail="NAVMO SPR for "+str(rank_details.reference_id)
				subject, from_email = subject_mail, 'noreplycodenicely@gmail.com'
				text_content = 'This is an important message.'
				template = get_template('email/email_content.html')
				msg = EmailMultiAlternatives(subject, text_content, from_email, ['bhirendra2014@gmail.com','noreplycodenicely@gmail.com','m3gh4l@gmail.com'])
				data['url_path']=url_path
				html_content  = template.render(RequestContext(request,data,))
				msg.attach_alternative(html_content, "text/html")
				msg.attach(filename,pdf,'application/pdf')
				msg.send()
				print "Email Sent for - ",rank_details.reference_id
				count+=1
				print "count = ",count
			except Exception,e:
				print "Exception on SPR Report : \n",e
				print "Exception occured for "+user_details.refrence_id
	except Exception,e:
		print "Outer Catch :",e
		# z.close()
		# response = HttpResponse(z, content_type='application/zip')
		# response['Content-Disposition'] = 'attachment; filename='+zip_file_name
	return HttpResponse("Email Sent")

#--------------------------------------------------------------------------
def download_spr_into(request,get_centre_name,get_group_name,url_path):
	json={}
	zip_file_name="SPR_"+get_centre_name+"_"+get_group_name+".zip"
	buffer= StringIO.StringIO()
	z = zipfile.ZipFile(buffer, "w")
	if get_centre_name!="all":
		if get_group_name!="all":
			marks_filter=marks_data.objects.filter(center=get_centre_name,group=get_group_name)
		else:
			marks_filter=marks_data.objects.filter(center=get_centre_name)
	else:
		if get_group_name!="all":
			marks_filter=marks_data.objects.filter(group=get_group_name)
		else:
			marks_filter=marks_data.objects.all()
	try:
		count=0;
		for marks_details in marks_filter:
			for rank_details in rank_data.objects.filter(reference_id=marks_details.reference_id,group=marks_details.group):				
				try:
					filepath=url_path+"/media/"
					# filename="navmo_spr_"+rank_details.reference_id+"_"+rank_details.level+".pdf"
					filename="navmo_spr_"+rank_details.reference_id+"_"+rank_details.level+".pdf"
					print "File Path = ",filepath
					# working_folder=url_path+"/media/"+rank_details.reference_id+"/"
					# files = os.listdir(working_folder)
					# for f in files:
					# 	if f[-3:] == 'pdf':
					# z.write(filename,zipfile.ZIP_DEFLATED)
					z.write(str(filename),str(filepath),compress_type = zipfile.ZIP_DEFLATED)
					print "successfully added",rank_details.reference_id," into zip"
					print z.namelist()
					count+=1
					print "Count = ",count
				except Exception,e:
					print "Exception on adding file into zip",e
		response = HttpResponse(z, content_type='application/zip')
		response['Content-Disposition'] = 'attachment; filename='+zip_file_name
		z.close()
		return response
	except Exception,e:
		print "Outer Catch ",e
		return "Exception Occured"


#==============Method is not in use anyhere==========================
#-------------It is Used to save generated pdf to server folder---------
# def save_spr_to_sever(request,get_centre_name,get_group_name,url_path):
def download_spr_into_pc(request,get_centre_name,get_group_name,url_path):
	filename=""
	json={}
	json['BASE_DIR']=BASE_DIR
	json['url_path']=url_path
	# zip_file_name="SPR_"+get_centre_name+"_"+get_group_name+".zip"
	# buffer= StringIO.StringIO()
	# z = zipfile.ZipFile(buffer, "w")

	#===putting data in html====
	#for rank_details in rank_data.objects.order_by('group','national_group_rank'):
	if get_centre_name!="all":
		if get_group_name!="all":
			marks_filter=marks_data.objects.filter(center=get_centre_name,group=get_group_name)
		else:
			marks_filter=marks_data.objects.filter(center=get_centre_name)
	else:
		if get_group_name!="all":
			marks_filter=marks_data.objects.filter(group=get_group_name)
		else:
			marks_filter=marks_data.objects.all()
	try:
		count=0;
		for marks_details in marks_filter:
			try :
				for rank_details in rank_data.objects.filter(reference_id=marks_details.reference_id,group=marks_details.group):
					try:
						filename="navmo_spr_"+rank_details.reference_id+"_"+rank_details.level+".pdf"
						print rank_details.reference_id
						user_details=user_data.objects.get(refrence_id=rank_details.reference_id)
						try:
							image_name=str(user_details.image).replace(" ","%20")
							path=url_path+"/media/"+image_name
							json['image']=path
							if "media" in image_name and "default" not in image_name:
								path=url_path+image_name
								json['image']=path
							if str(user_details.image)==(str(user_details.refrence_id)+"/image") or str(user_details.image)=="/media/default.png":
								path=url_path+"/media/icon.png"
								json['image']=path
							print "Image Path = ",path
						except Exception,e:
							print "Exception on image :",e
							path=url_path+"/media/"+"icon.png"
							json['image']=path
						json['reference_id']=rank_details.reference_id
						json['name']=(str(user_details.first_name+' '+user_details.last_name)).title()
						if (user_details.last_name).lower() in (user_details.parent_father).lower():
							father=(user_details.parent_father).title()
						else:
							father=(user_details.parent_father+" "+user_details.last_name).title()
						json['father']=father
						json['class']=(str(user_details.grade)).title()
						school=""
						if "icis" in (user_details.school).lower() or "cadet" in (user_details.school).lower() or "i c i" in (user_details.school).lower() or "ici school" in (user_details.school).lower():
							school="Intelligent Cadet International School"
						elif "goel" in (user_details.school).lower() or "n h" in (user_details.school).lower() or "nh" in (user_details.school).lower() or "n.h." in (user_details.school).lower():
							school="N H Goel World School"
						elif "birla" in (user_details.school).lower():
							school="B K Birla Centre For Education"
						elif "atelier" in (user_details.school).lower():
							school="Atelier International Preschool"
						elif "vibgyor" in (user_details.school).lower():
							school="Vibgyor High School"
						elif "tree" in (user_details.school).lower() or "house" in (user_details.school).lower():
							school="Tree House High School"
						elif "gumla" in (user_details.school).lower():
							school="D.A.V.Public School"
						elif "podar" in (user_details.school).lower():
							school="Podar International School"
						else:
							school=str(user_details.school).title()
						json['school']=school
					except Exception,e:
						print e
						json['name']="Not Available"
						json['father']="Not Available"
						json['class']="Not Available"
						json['school']="Not Available"
					json['level']=(rank_details.level).title()
					marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
					json['round']=marks_details.current_round
					if marks_details.current_round=='Finals':
						if marks_details.npi_final!=0:
							json['round']=marks_details.current_round
							json['marks']=marks_details.marks_final
							json['time']=marks_details.time_final
							json['npi']=marks_details.npi_final
						else:
							json['round']="Semi-Finals"
							json['marks']=marks_details.marks_semi
							json['time']=marks_details.time_semi
							json['npi']=marks_details.npi_semi
					elif marks_details.current_round=='Semi-Finals':
						json['round']=marks_details.current_round
						json['marks']=marks_details.marks_semi
						json['time']=marks_details.time_semi
						json['npi']=marks_details.npi_semi
					elif marks_details.current_round=='First-Round':
						json['round']=marks_details.current_round
						json['marks']=marks_details.marks_first
						json['time']=marks_details.time_first
						json['npi']=marks_details.npi_first		

					marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
					json['centre_rank']=rank_details.centre_rank
					json['national_level_rank']=rank_details.national_level_rank
					json['national_group_rank']=rank_details.national_group_rank
					try:
						#===================send html to PDF form =======================
						options = {
						'margin-left':'0',
						'margin-right':'0',
						'margin-top':'0',
						'margin-bottom':'0'}
						template=get_template("spr_report/spr_a4.html")
						context = Context(json)  # data is the context data that is sent to the html file to render the output. 
						html = template.render(context)  # Renders the template with the context data.
						pdf=pdfkit.from_string(html, False,options=options)
						response = HttpResponse(pdf,content_type='application/pdf')
						response['Content-Disposition'] = 'attachment; filename='+filename
						# try:
						# 	folder = 'media/'+rank_details.reference_id+'/'
						# 	fout = open(folder+filename, 'w')
						# 	fout.write(pdf)
						# 	fout.close()
						# except Exception,e:
						# 	if "No such file or directory" in e:
						# 		print "Folder Created"
						# 		while True:
						# 			try:
						# 				folder = 'media/'+rank_details.reference_id+'/'
						# 				os.mkdir(os.path.join(folder))
						# 				break
						# 			except Exception,e:
						# 				print e
						# 		folder = 'media/'+rank_details.reference_id+'/'		
						# 		fout = open(folder+filename, 'w')
						# 		fout.write(pdf)
						# 		fout.close()
						# 	else:
						# 		print "Exception on exporting pdf : ",e
						try:
							folder = 'media/'+get_centre_name+'/'
							if not os.path.exists(folder):
								while True:
									try:
										os.mkdir(os.path.join(folder))
										print "Folder Created"
										break
									except Exception,e:
										print "Exception on folder creation : ",e
							fout = open(folder+filename, 'w')
							fout.write(pdf)
							fout.close()
							print "successfully Added",rank_details.reference_id
						except Exception,e:
							print "Exception on write file into Folder : ",e
							
						# response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response
						# js=response.read().decode('utf-8')s
						# buffer_response=json.loads(response.content.decode('utf-8'))
						# buffer_response=response.content.decode('UTF-8')
						# print buffer_response
						# z.writestr(filename,pdf)
						# print z.getinfo()
						# print z.namelist()
						# print "successfully added",rank_details.reference_id," into zip"
						count+=1
						print count
					except Exception,e:
						print "Exception on SPR Report : \n",e
						print "Exception occured for "+user_details.refrence_id
			except Exception,e:
				print e
		# z.close()
		# response = HttpResponse(z, content_type='application/zip')
		# response['Content-Disposition'] = 'attachment; filename='+zip_file_name
		return HttpResponseRedirect('/download_spr_panel')
	except Exception,e:
		print "Outer Catch ",e
		return "Exception Occured"
@login_required
def download_spr_for_user(request):
	get_ref_id=str(request.user)
	get_level=request.session.get('level_name')
	print get_level
	json={}
	url_path=str(request.scheme+"://"+request.get_host())
	json['BASE_DIR']=BASE_DIR
	json['url_path']=url_path
	for rank_details in rank_data.objects.filter(reference_id=get_ref_id,level=get_level):
		try:
			filename="navmo_spr_"+rank_details.reference_id+"_"+rank_details.level+".pdf"
			print rank_details.reference_id
			user_details=user_data.objects.get(refrence_id=rank_details.reference_id)
			try:
				image_name=str(user_details.image).replace(" ","%20")
				path=url_path+"/media/"+image_name
				json['image']=path
				if "media" in image_name and "default" not in image_name:
					path=url_path+image_name
					json['image']=path
				if str(user_details.image)==(str(user_details.refrence_id)+"/image") or str(user_details.image)=="/media/default.png":
					path=url_path+"/media/icon.png"
					json['image']=path
				print "Image Path = ",path
			except Exception,e:
				print "Exception on image :",e
				path=url_path+"/media/"+"icon.png"
				json['image']=path
			json['reference_id']=rank_details.reference_id
			json['name']=(str(user_details.first_name+' '+user_details.last_name)).title()
			if (user_details.last_name).lower() in (user_details.parent_father).lower():
				father=(user_details.parent_father).title()
			else:
				father=(user_details.parent_father+" "+user_details.last_name).title()
			json['father']=father
			json['class']=(str(user_details.grade)).title()
			school=""
			if "icis" in (user_details.school).lower() or "cadet" in (user_details.school).lower() or "i c i" in (user_details.school).lower() or "ici school" in (user_details.school).lower():
				school="Intelligent Cadet International School"
			elif "goel" in (user_details.school).lower() or "n h" in (user_details.school).lower() or "nh" in (user_details.school).lower() or "n.h." in (user_details.school).lower():
				school="N H Goel World School"
			elif "birla" in (user_details.school).lower():
				school="B K Birla Centre For Education"
			elif "atelier" in (user_details.school).lower():
				school="Atelier International Preschool"
			elif "vibgyor" in (user_details.school).lower():
				school="Vibgyor High School"
			elif "tree" in (user_details.school).lower() or "house" in (user_details.school).lower():
				school="Tree House High School"
			elif "gumla" in (user_details.school).lower():
				school="D.A.V.Public School"
			elif "podar" in (user_details.school).lower():
				school="Podar International School"
			else:
				school=str(user_details.school).title()
			json['school']=school
		except Exception,e:
			print e
			json['name']="Not Available"
			json['father']="Not Available"
			json['class']="Not Available"
			json['school']="Not Available"
		json['level']=(rank_details.level).title()
		marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
		json['round']=marks_details.current_round
		if marks_details.current_round=='Finals':
			if marks_details.npi_final!=0:
				json['round']=marks_details.current_round
				json['marks']=marks_details.marks_final
				json['time']=marks_details.time_final
				json['npi']=marks_details.npi_final
			else:
				json['round']="Semi-Finals"
				json['marks']=marks_details.marks_semi
				json['time']=marks_details.time_semi
				json['npi']=marks_details.npi_semi
		elif marks_details.current_round=='Semi-Finals':
			json['round']=marks_details.current_round
			json['marks']=marks_details.marks_semi
			json['time']=marks_details.time_semi
			json['npi']=marks_details.npi_semi
		elif marks_details.current_round=='First-Round':
			json['round']=marks_details.current_round
			json['marks']=marks_details.marks_first
			json['time']=marks_details.time_first
			json['npi']=marks_details.npi_first		

		marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
		json['centre_rank']=rank_details.centre_rank
		json['national_level_rank']=rank_details.national_level_rank
		json['national_group_rank']=rank_details.national_group_rank
		try:
			#===================send html to PDF form =======================
			options = {
			# 'page-width':'656.166667',
			# 'page-height':'928.158333',
			'margin-left':'0',
			'margin-right':'0',
			'margin-top':'0',
			'margin-bottom':'0'}
			template=get_template("spr_report/spr_a4.html")
			context = Context(json)  # data is the context data that is sent to the html file to render the output. 
			html = template.render(context)  # Renders the template with the context data.
			pdf=pdfkit.from_string(html, False,options=options)
			response = HttpResponse(pdf,content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename='+file_name
		except Exception,e:
			print "Exception on PDF",e
	return response
def convert_to_pdf(request,get_centre_name,get_group_name,url_path):
	filename=""
	json={}
	json['BASE_DIR']=BASE_DIR
	json['url_path']=url_path
	#===putting data in html====
	#for rank_details in rank_data.objects.order_by('group','national_group_rank'):
	if get_centre_name!="all":
		if get_group_name!="all":
			marks_filter=marks_data.objects.filter(center=get_centre_name,group=get_group_name)
		else:
			marks_filter=marks_data.objects.filter(center=get_centre_name)
	else:
		if get_group_name!="all":
			marks_filter=marks_data.objects.filter(group=get_group_name)
		else:
			marks_filter=marks_data.objects.all()
	try:
		count=0;
		for marks_details in marks_filter:
			try :
				for rank_details in rank_data.objects.filter(reference_id=marks_details.reference_id,group=marks_details.group):
					try:
						filename="navmo_spr_"+rank_details.reference_id+"_"+rank_details.level+".pdf"
						print rank_details.reference_id
						user_details=user_data.objects.get(refrence_id=rank_details.reference_id)
						try:
							image_name=str(user_details.image).replace(" ","%20")
							path=url_path+"/media/"+image_name
							json['image']=path
							if "media" in image_name and "default" not in image_name:
								path=url_path+image_name
								json['image']=path
							if str(user_details.image)==(str(user_details.refrence_id)+"/image") or str(user_details.image)=="/media/default.png":
								path=url_path+"/media/icon.png"
								json['image']=path
							print "Image Path = ",path
						except Exception,e:
							print "Exception on image :",e
							path=url_path+"/media/"+"icon.png"
							json['image']=path
						json['reference_id']=rank_details.reference_id
						json['name']=(str(user_details.first_name+' '+user_details.last_name)).title()
						if (user_details.last_name).lower() in (user_details.parent_father).lower():
							father=(user_details.parent_father).title()
						else:
							father=(user_details.parent_father+" "+user_details.last_name).title()
						json['father']=father
						json['class']=(str(user_details.grade)).title()
						school=""
						if "icis" in (user_details.school).lower() or "cadet" in (user_details.school).lower() or "i c i" in (user_details.school).lower() or "ici school" in (user_details.school).lower():
							school="Intelligent Cadet International School"
						elif "goel" in (user_details.school).lower() or "n h" in (user_details.school).lower() or "nh" in (user_details.school).lower() or "n.h." in (user_details.school).lower():
							school="N H Goel World School"
						elif "birla" in (user_details.school).lower():
							school="B K Birla Centre For Education"
						elif "atelier" in (user_details.school).lower():
							school="Atelier International Preschool"
						elif "vibgyor" in (user_details.school).lower():
							school="Vibgyor High School"
						elif "tree" in (user_details.school).lower() or "house" in (user_details.school).lower():
							school="Tree House High School"
						elif "gumla" in (user_details.school).lower():
							school="D.A.V.Public School"
						elif "podar" in (user_details.school).lower():
							school="Podar International School"
						else:
							school=str(user_details.school).title()
						json['school']=school
					except Exception,e:
						print e
						json['name']="Not Available"
						json['father']="Not Available"
						json['class']="Not Available"
						json['school']="Not Available"
					json['level']=(rank_details.level).title()
					marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
					json['round']=marks_details.current_round
					if marks_details.current_round=='Finals':
						if marks_details.npi_final!=0:
							json['round']=marks_details.current_round
							json['marks']=marks_details.marks_final
							json['time']=marks_details.time_final
							json['npi']=marks_details.npi_final
						else:
							json['round']="Semi-Finals"
							json['marks']=marks_details.marks_semi
							json['time']=marks_details.time_semi
							json['npi']=marks_details.npi_semi
					elif marks_details.current_round=='Semi-Finals':
						json['round']=marks_details.current_round
						json['marks']=marks_details.marks_semi
						json['time']=marks_details.time_semi
						json['npi']=marks_details.npi_semi
					elif marks_details.current_round=='First-Round':
						json['round']=marks_details.current_round
						json['marks']=marks_details.marks_first
						json['time']=marks_details.time_first
						json['npi']=marks_details.npi_first		

					marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
					json['centre_rank']=rank_details.centre_rank
					json['national_level_rank']=rank_details.national_level_rank
					json['national_group_rank']=rank_details.national_group_rank
					try:
						#===================send html to PDF form =======================
						options = {
						# 'page-width':'656.166667',
						# 'page-height':'928.158333',
						'margin-left':'0',
						'margin-right':'0',
						'margin-top':'0',
						'margin-bottom':'0'}
						template=get_template("spr_report/spr_a4.html")
						context = Context(json)  # data is the context data that is sent to the html file to render the output. 
						html = template.render(context)  # Renders the template with the context data.
						pdf=pdfkit.from_string(html, False,options=options)
						response = HttpResponse(content_type='application/pdf')
						response['Content-Disposition'] = 'attachment; filename='+filename
						data={}
						data['msg']="Dear "+str(user_details.first_name)+",<br>"+"Thank You for participating in NAVMO 2016-17. We would like to congratulate you on your achievement and we hope that you enjoyed NAVMO and learn something.<br> We are proud to launch Student Performance Report for NAVMO 2016-17. Report can be downloaded by login into your account at www.mpenavmo.com and we are also attaching a copy of your SPR Report along with this mail.<br><br> We hope that you will be a part of NAVMO 2017-18. For any further updates please visit www.mpenavmo.com<br><br><br>Thanks<br> Team NAVMO<br> MIND POWER EDUCATION Family"
						data['msg_head']="NAVMO 2016-17"
						text_content ='This is an important message.'
						from_email='noreplycodenicely@gmail.com'
						try:
							user_details=user_data.objects.get(refrence_id=rank_details.reference_id)
							user_email=user_details.email
							to_email=['bhirendra2014@gmail.com','m3gh4l@gmail.com','educate1996@gmail.com']
							subject='NAVMO 2016-17 Student Performance Report'
						except Exception,e:
							print "Exception on Email-Id : ",user_details.refrence_id
							to_email=['bhirendra2014@gmail.com','m3gh4l@gmail.com']
							subject='SPR : Error in Email'
						template = get_template('email/email_content.html')
						msg = EmailMultiAlternatives(subject, text_content, from_email,to_email)
						data['url_path']=url_path
						html_content  = template.render(RequestContext(request,data,))
						msg.attach_alternative(html_content, "text/html")
						msg.attach(filename,pdf,'application/pdf')
						msg.send()
						print "Email Sent for - ",rank_details.reference_id
						count+=1
						print "count = ",count
					except Exception,e:
						print "Exception on SPR Report : \n",e
						print "Exception occured for "+user_details.refrence_id
			except Exception,e:
				print e
		return "success"
	except Exception,e:
		print "Outer Catch ",e
		return "Exception Occured"
	#return render(request,"spr_report/spr_message.html",json)
	#-----Inline Image------------
			# msg.mixed_subtype='related'
			# for f in ['/media/top1.jpg', '/navmo/templates/spr_report/divider.png']:
			#     fp = open(BASE_DIR+f, 'rb')
			#     msg_img = MIMEImage(fp.read())
			#     fp.close()
			#     msg_img.add_header('Content-ID', "inline".format(f))
			    #msg.attach(msg_img)
			#-----------------------------
	# #===================================================
	# #=======Convert to pdf and Send to email============
	# #===================================================
	# pdf=pdfkit.from_url('http://www.google.co.in',False)
	# response = HttpResponse(content_type='application/pdf')
	# response['Content-Disposition'] = 'attachment; filename="spr_demo.pdf"'
	# EmailMsg=EmailMessage("NAVMO Student Performance Report ","Here we are Attaching your SPR Report of NAVMO 2016-17 ",'noreplycodenicely@gmail.com',['bhirendra2014@gmail.com'])
	# EmailMsg.attach('spr_demo.pdf',pdf,'application/pdf')
	# EmailMsg.send()
	# print "Email Sent"
	# return HttpResponse("Email Sent")
	#===================================================

	# #=======Convert to pdf and Open it===============================
	# pdfkit.from_url('http://www.google.co.in',"spr_demo.pdf")
	# pdf = open("spr_demo.pdf")
	# response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
	# response['Content-Disposition'] = 'attachment; filename=spr_demo.pdf'
	# pdf.close()
	# os.remove("spr_demo.pdf")  # remove the locally created pdf file.
	# return response  # returns the response.
	# #================================================================

# National Rank List
#=============================================================================================
def national_all_rank_levelwise(request):
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
					if topper_marks_final!=0.0 and marks_details.marks_final!=0.0:
						try:
							temp3=marks_details.marks_final/topper_marks_final
							minutes=int(marks_details.time_final)
							seconds=marks_details.time_final-minutes
							time=(minutes*60)+(seconds*100)
							time=time/60
							temp3=temp3/time# marks_details.npi_semi=temp1
							temp3=temp3*250

							if(group[0]=='alpha'):
								temp3=temp3*2
							elif(group[0]=='thetha'):
								temp3=temp3*4							
							setattr(marks_details,'npi_final',"%.2f" % temp3)
							marks_details.save()
						except Exception,e:
							print e
						print 'Final Round'
					elif topper_marks_semi!=0.0 and marks_details.marks_semi!=0.0:
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
	for level in level_list.order_by('level'):
		count=1
		result_data+='<div class="row"><div class="col s12 m0 "></div><div class="col s12 m12"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
		result_data+='Rank List '
		result_data+=str(level[0])+' '
		result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Id">Name</th><th id="th" data-field="Id">Group-Level</th><th id="th" data-field="Id">Round</th><th id="th" data-field="Id">Marks</th><th id="th" data-field="Id">Time</th><th id="th" data-field="Id">NPI Score</th></tr></thead>'
		result_data+='<tbody id="'+str(level[0])+'">'
		print group[0]
		for groups_data in marks_data.objects.filter(level=level[0],current_round='Finals').order_by('-npi_final'):
			if groups_data.marks_final!=0.0 and groups_data.npi_final!=0.0:
				result_data+='<tr><td id="td">'+str(count)+'</td>'
				result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
				try:
					user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
					result_data+='<td id="td">'+(str(user_details.first_name+' '+user_details.last_name)).upper()+'</td>'
				except Exception,e:
					result_data+='<td id="td">'+"Not Available"+'</td>'
					print e
				result_data+='<td id="td">'+str(groups_data.level)+'</td>'
				result_data+='<td id="td">'+str(groups_data.current_round)+'</td>'
				result_data+='<td id="td">'+str(groups_data.marks_final)+'</td>'
				result_data+='<td id="td">'+str(groups_data.time_final)+'</td>'
				result_data+='<td id="td">'+str(groups_data.npi_final)+'</td></tr>'
				rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
				rank_details.national_level_rank=count
				rank_details.save()
				count+=1
				print groups_data.reference_id
		#-----------------------------------------------------------------------
		# Print absent national students with their semi NPI and round semifinal 
		#------------------------------------------------------------------------
		for groups_data in marks_data.objects.filter(level=level[0],current_round='Finals').order_by('-npi_semi'):
			if groups_data.npi_final==0.0:
				result_data+='<tr><td id="td">'+str(count)+'</td>'
				result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
				try:
					user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
					result_data+='<td id="td">'+(str(user_details.first_name+' '+user_details.last_name)).upper()+'</td>'
				except Exception,e:
					result_data+='<td id="td">'+"Not Available"+'</td>'
					print e
				result_data+='<td id="td">'+str(groups_data.level)+'</td>'
				result_data+='<td id="td">'+"Semi-Finals"+'</td>'
				result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
				result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
				result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td></tr>'
				rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
				rank_details.national_level_rank=count
				rank_details.save()
				count+=1
				print groups_data.reference_id
		#------------------------------------------------------------------------
		for groups_data in marks_data.objects.filter(level=level[0],current_round='Semi-Finals').order_by('-npi_semi'):
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			try:
				user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
				result_data+='<td id="td">'+(str(user_details.first_name+' '+user_details.last_name)).upper()+'</td>'
			except Exception,e:
				result_data+='<td id="td">'+"Not Available"+'</td>'
				print e
			result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			result_data+='<td id="td">'+str(groups_data.current_round)+'</td>'
			result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
			result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
			result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td></tr>'
			rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
			rank_details.national_level_rank=count
			rank_details.save()
			count+=1
			print groups_data.reference_id
		for groups_data in marks_data.objects.filter(level=level[0],current_round='First-Round').order_by('-npi_first'):
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			try:
				user_details=user_data.objects.get(refrence_id=str(groups_data.reference_id))
				result_data+='<td id="td">'+(str(user_details.first_name+' '+user_details.last_name)).upper()+'</td>'
			except Exception,e:
				result_data+='<td id="td">'+"Not Available"+'</td>'
				print e
			result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			result_data+='<td id="td">'+str(groups_data.current_round)+'</td>'
			result_data+='<td id="td">'+str(groups_data.marks_first)+'</td>'
			result_data+='<td id="td">'+str(groups_data.time_first)+'</td>'
			result_data+='<td id="td">'+str(groups_data.npi_first)+'</td></tr>'
			rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
			rank_details.national_level_rank=count
			rank_details.save()
			count+=1
			print groups_data.reference_id
		result_data+='</tbody></table></div></ul></div></div></div></div>'
	try:
		return render(request,'results/admin_results.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/admin_results.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})
#---------------------------------------------------------------------------------------------
def national_all_rank_groupwise(request):
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
						temp3=marks_details.marks_final/topper_marks_final
						minutes=int(marks_details.time_final)
						seconds=marks_details.time_final-minutes
						time=(minutes*60)+(seconds*100)
						time=time/60
						temp3=temp3/time# marks_details.npi_semi=temp1
						temp3=temp3*250

						if(group[0]=='alpha'):
							temp3=temp3*2
						elif(group[0]=='thetha'):
							temp3=temp3*4							
						setattr(marks_details,'npi_final',"%.2f" % temp3)
						marks_details.save()
					except Exception,e:
						print e
					print 'Final Round'
				elif topper_marks_semi!=0.0 and marks_details.marks_semi!=0.0:
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
	for group in marks_data.objects.order_by('group').values_list('group').distinct():
		count=1
		result_data+='<div class="row"><div class="col s12 m0 "></div><div class="col s12 m12"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
		result_data+='Rank List '
		result_data+=str(group[0])+' '
		result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Id">Name</th><th id="th" data-field="Id">Center</th><th id="th" data-field="Id">Group-Level</th><th id="th" data-field="Id">Round</th><th id="th" data-field="Id">Marks</th><th id="th" data-field="Id">Time</th><th id="th" data-field="Id">NPI Score</th></tr></thead>'
		result_data+='<tbody id="'+str(group[0])+'">'
		print group[0]
		for groups_data in marks_data.objects.filter(group=group[0],current_round='Finals').order_by('-npi_final'):
			if groups_data.marks_final!=0.0 and groups_data.npi_final!=0.0:
				result_data+='<tr><td id="td">'+str(count)+'</td>'
				result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
				try:
					user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
					result_data+='<td id="td">'+str(user_details.first_name+' '+user_details.last_name)+'</td>'
				except Exception,e:
					print e
					result_data+='<td id="td">'+"N A"+'</td>'
				result_data+='<td id="td">'+str(groups_data.center)+'</td>'
				result_data+='<td id="td">'+str(groups_data.level)+'</td>'
				result_data+='<td id="td">'+str(groups_data.current_round)+'</td>'
				result_data+='<td id="td">'+str(groups_data.marks_final)+'</td>'
				result_data+='<td id="td">'+str(groups_data.time_final)+'</td>'
				result_data+='<td id="td">'+str(groups_data.npi_final)+'</td></tr>'
				# try:
				# 	rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
				# 	rank_details.national_group_rank=count
				# 	rank_details.save()
				# except Exception,e:
				# 	b=rank_data(reference_id=groups_data.reference_id,group=groups_data.group,level=groups_data.level,national_group_rank=count)
				# 	b.save()
				# count+=1
				print groups_data.reference_id
		for groups_data in marks_data.objects.filter(group=group[0],current_round='Finals').order_by('-npi_semi'):
			if groups_data.npi_final==0.0:
				result_data+='<tr><td id="td">'+str(count)+'</td>'
				result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
				try:
					user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
					result_data+='<td id="td">'+str(user_details.first_name+' '+user_details.last_name)+'</td>'
				except Exception,e:
					print e
					result_data+='<td id="td">'+"N A"+'</td>'
				result_data+='<td id="td">'+str(groups_data.center)+'</td>'
				result_data+='<td id="td">'+str(groups_data.level)+'</td>'
				result_data+='<td id="td">'+"Semi-Finals"+'</td>'
				result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
				result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
				result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td></tr>'
				# try:
				# 	rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
				# 	rank_details.national_group_rank=count
				# 	rank_details.save()
				# except Exception,e:
				# 	b=rank_data(reference_id=groups_data.reference_id,group=groups_data.group,level=groups_data.level,national_group_rank=count)
				# 	b.save()
				count+=1
				print groups_data.reference_id
		for groups_data in marks_data.objects.filter(group=group[0],current_round='Semi-Finals').order_by('-npi_semi'):
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			try:
				user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
				result_data+='<td id="td">'+str(user_details.first_name+' '+user_details.last_name)+'</td>'
			except Exception,e:
				print e
				result_data+='<td id="td">'+"N A"+'</td>'
			result_data+='<td id="td">'+str(groups_data.center)+'</td>'
			result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			result_data+='<td id="td">'+str(groups_data.current_round)+'</td>'
			result_data+='<td id="td">'+str(groups_data.marks_semi)+'</td>'
			result_data+='<td id="td">'+str(groups_data.time_semi)+'</td>'
			result_data+='<td id="td">'+str(groups_data.npi_semi)+'</td></tr>'
			# try:
			# 	rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
			# 	rank_details.national_group_rank=count
			# 	rank_details.save()
			# except Exception,e:
			# 	b=rank_data(reference_id=groups_data.reference_id,group=groups_data.group,level=groups_data.level,national_group_rank=count)
			# 	b.save()
			count+=1
			print groups_data.reference_id
		for groups_data in marks_data.objects.filter(group=group[0],current_round='First-Round').order_by('-npi_first'):
			result_data+='<tr><td id="td">'+str(count)+'</td>'
			result_data+='<td id="td">'+str(groups_data.reference_id)+'</td>'
			try:
				user_details=user_data.objects.get(refrence_id=groups_data.reference_id)
				result_data+='<td id="td">'+str(user_details.first_name+' '+user_details.last_name)+'</td>'
			except Exception,e:
				print e
				result_data+='<td id="td">'+"N A"+'</td>'
			result_data+='<td id="td">'+str(groups_data.center)+'</td>'
			result_data+='<td id="td">'+str(groups_data.level)+'</td>'
			result_data+='<td id="td">'+str(groups_data.current_round)+'</td>'
			result_data+='<td id="td">'+str(groups_data.marks_first)+'</td>'
			result_data+='<td id="td">'+str(groups_data.time_first)+'</td>'
			result_data+='<td id="td">'+str(groups_data.npi_first)+'</td></tr>'
			# try:
			# 	rank_details=rank_data.objects.get(reference_id=groups_data.reference_id,level=groups_data.level)
			# 	rank_details.national_group_rank=count
			# 	rank_details.save()
			# except Exception,e:
			# 	b=rank_data(reference_id=groups_data.reference_id,group=groups_data.group,level=groups_data.level,national_group_rank=count)
			# 	b.save()
			count+=1
			print groups_data.reference_id
		result_data+='</tbody></table></div></ul></div></div></div></div>'
	try:
		return render(request,'results/admin_results.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'results/admin_results.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})

def spr_report(request):

	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'

	if(request.method=="GET"):
		return render(request,'spr_report/spr_main.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})

	if(request.method=="POST"):
		get_centre=str(request.POST.get('centre'))
		print get_centre
		get_group=str(request.POST.get('group'))
		print get_group		
		if get_centre!="all":
			if get_group!="all":
				marks_list =marks_data.objects.filter(center=get_centre, group=get_group).order_by().distinct()
			else:
				marks_list =marks_data.objects.filter(center=get_centre).order_by('group').distinct()
		else:
			if get_group!="all":
				marks_list =marks_data.objects.filter(group=get_group).order_by('center').distinct()	
			else:
				marks_list =marks_data.objects.all()

		result_data=''
		try :
			for marks_details in marks_list:
				for rank_details in rank_data.objects.filter(reference_id=marks_details.reference_id,group=marks_details.group):
					result_data+='<div class="row"><div class="col s12 m3 "></div><div class="col s12 m6"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text">'
					result_data+='<div class="responsive-table"><table id="table"><th id="th" colspan=3><img src="/media/mpe_logo.jpg" width="120" height="50" style="float:left"></img><img src="/media/navmo.jpg" width="100" height="50" style="float:right"></img><h5 style="text-align:center">Student Performance Report</h5></th>'
					result_data+='<tr><td id ="td" rowspan="8" style="width:30%"><center><img src="'
		
					# Image path
					try:
						user_details=user_data.objects.get(refrence_id=rank_details.reference_id)
						result_data+="/media/"+str(user_details.image)
					except Exception,e:
						print e
					
					result_data+='" height="176" width="132"></img></center></td>'
					
					result_data+='<td id ="td" style="width:35%">'+"Reference Id :"+'</td>'
					result_data+='<td id ="td"><strong>'+str(rank_details.reference_id)+'</strong></td></tr>'
					try:
						user_details=user_data.objects.get(refrence_id=rank_details.reference_id)
						result_data+='<tr><td id ="td" style="width:35%">'+"Name  :"+'</td>'
						result_data+='<td id ="td"><strong>'+(str(user_details.first_name+' '+user_details.last_name)).title()+'</strong></td></tr>'
						
						result_data+='<tr><td id ="td" style="width:35%">'+"Father  :"+'</td>'
						result_data+='<td id ="td"><strong>'+(str(user_details.parent_father)).title()+'</strong></td></tr>'

						result_data+='<tr><td id ="td" style="width:35%">'+"Grade  :"+'</td>'
						result_data+='<td id ="td"><strong>'+str(user_details.grade)+'</strong></td></tr>'

						result_data+='<tr><td id ="td" style="width:35%">'+"School  :"+'</td>'
						result_data+='<td id ="td"><strong>'+(str(user_details.school)).title()+'</strong></td></tr>'
					except Exception,e:
						print e
						result_data+='<tr><td id ="td" style="width:35%">'+"Name  :"+'</td>'
						result_data+='<td id ="td"><strong>'+"N A"+'</strong></td></tr>'
						result_data+='<tr><td id ="td" style="width:35%">'+"Father  :"+'</td>'
						result_data+='<td id ="td"><strong>'+"N A"+'</strong></td></tr>'
						result_data+='<tr><td id ="td" style="width:35%">'+"Grade  :"+'</td>'
						result_data+='<td id ="td"><strong>'+"N A"+'</strong></td></tr>'
						result_data+='<tr><td id ="td" style="width:35%">'+"School  :"+'</td>'
						result_data+='<td id ="td"><strong>'+"N A"+'</strong></td></tr>'
					
					result_data+='<tr><td id ="td" style="width:35%">'+"Group-Level  :"+'</td>'
					result_data+='<td id ="td"><strong>'+str(rank_details.level)+'</strong></td></tr>'
					try:
						marks_details=marks_data.objects.get(reference_id=rank_details.reference_id, level=rank_details.level)
					except Exception,e:
						print e
					result_data+='<tr><td id ="td" style="width:35%">'+"Current-Round  :"+'</td>'
					if marks_details.current_round=='Finals':
						if marks_details.npi_final!=0:
							result_data+='<td id ="td"><strong>'+str(marks_details.current_round)+'</strong></td></tr>'
							result_data+='<tr><td id ="td" style="width:35%">'+"NPI Score  :"+'</td>'
							result_data+='<td id ="td"><strong>'+str(marks_details.npi_final)+'</strong></td></tr>'
						else:
							result_data+='<td id ="td"><strong>'+"Semi-Finals"+'</strong></td></tr>'
							result_data+='<tr><td id ="td" style="width:35%">'+"NPI Score  :"+'</td>'
							result_data+='<td id ="td"><strong>'+str(marks_details.npi_semi)+'</strong></td></tr>'
					elif marks_details.current_round=='Semi-Finals':
						result_data+='<td id ="td"><strong>'+str(marks_details.current_round)+'</strong></td></tr>'
						result_data+='<tr><td id ="td" style="width:35%">'+"NPI Score  :"+'</td>'
						result_data+='<td id ="td"><strong>'+str(marks_details.npi_semi)+'</strong></td></tr>'
					elif marks_details.current_round=='First-Round':
						result_data+='<td id ="td"><strong>'+str(marks_details.current_round)+'</strong></td></tr>'
						result_data+='<tr><td id ="td" style="width:35%">'+"NPI Score  :"+'</td>'
						result_data+='<td id ="td"><strong>'+str(marks_details.npi_first)+'</strong></td></tr>'

					result_data+='<tr><td id ="td"><center><strong>'+"Centre Rank"+'</strong></center></td>'
					result_data+='<td id ="td" ><center><strong>'+"National Group Rank"+'</strong></center></td>'
					result_data+='<td id ="td" ><center><strong>'+"National Level Rank"+'</strong></center></td></tr>'

					result_data+='<tr><td id ="td"><center><strong>'+str(rank_details.centre_rank)+'</strong></center></td>'
					result_data+='<td id ="td"><center><strong>'+str(rank_details.national_group_rank)+'</strong></center></td>'
					result_data+='<td id ="td"><center><strong>'+str(rank_details.national_level_rank)+'</strong></td></center></tr>'
					
					result_data+='</table></div></div></div></div></div>'
			return render(request,'spr_report/spr_main.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})
		except Exception,e:
			print e
			return render(request,'spr_report/spr_main.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})

def generate(max_first,max_semi,get_group):	
	set_id=1700376
	if get_group=="thetha":
		# for i in range(1,int(max_first)):
		# 	num=random.randint(0,1)
		# 	set_level=""
		# 	if num==0:
		# 		set_level="thetha-1"
		# 	elif num==1:
		# 		set_level="thetha-2"
		# 	p=marks_data(reference_id=set_id,group=get_group,current_round='First-Round',level=set_level,center='MPE KOTA',marks_first=float(i),time_first=20.0)
		# 	p.save()
		# 	set_id+=1
		for i in range(1,int(max_semi)):
			num=random.randint(0,1)
			set_level=""
			if num==0:
				set_level="thetha-1"
			elif num==1:
				set_level="thetha-2"
			p=marks_data(reference_id=set_id,group=get_group,current_round='Semi-Finals',level=set_level,center='MPE KOTA',marks_semi=float(i),time_semi=20.0)
			p.save()
			set_id+=1
	# if get_group=="gamma":
		# for i in range(1,int(max_first)):
		# 	num=random.randint(0,6)
		# 	set_level=""
		# 	set_time=0.0
		# 	if num==0:
		# 		set_level="MM-1A"
		# 		set_time=10.0
		# 	elif num==1:
		# 		set_level="MM-1B"
		# 		set_time=5.0
		# 	elif num==2:
		# 		set_level="MM-1C"
		# 		set_time=5.0
		# 	elif num==3:
		# 		set_level="MM-2"
		# 		set_time=5.0
		# 	elif num==4:
		# 		set_level="MM-3"
		# 		set_time=5.0
		# 	elif num==5:
		# 		set_level="MM-4"
		# 		set_time=5.0
		# 	elif num==6:
		# 		set_level="MM-5"
		# 		set_time=5.0
		# 	p=marks_data(reference_id=set_id,group=get_group,current_round='First-Round',level=set_level,center='MPE KOTA',marks_first=float(i),time_first=set_time)
		# 	p.save()
		# 	set_id+=1
		# for i in range(1,int(max_semi)):
		# 	num=random.randint(0,6)
		# 	set_level=""
		# 	set_time=0.0
		# 	if num==0:
		# 		set_level="MM-1A"
		# 		set_time=10.0
		# 	elif num==1:
		# 		set_level="MM-1B"
		# 		set_time=5.0
		# 	elif num==2:
		# 		set_level="MM-1C"
		# 		set_time=5.0
		# 	elif num==3:
		# 		set_level="MM-2"
		# 		set_time=5.0
		# 	elif num==4:
		# 		set_level="MM-3"
		# 		set_time=5.0
		# 	elif num==5:
		# 		set_level="MM-4"
		# 		set_time=5.0
		# 	elif num==6:
		# 		set_level="MM-5"
		# 		set_time=5.0
		# 	p=marks_data(reference_id=set_id,group=get_group,current_round='Semi-Finals',level=set_level,center='MPE KOTA',marks_semi=float(i),time_semi=set_time)
		# 	p.save()
		# 	set_id+=1
	# if get_group=="beta":
		# for i in range(1,int(max_first)):
		# 	num=random.randint(0,4)
		# 	set_level=""
		# 	if num==0:
		# 		set_level="beta1"
		# 	elif num==1:
		# 		set_level="beta2"
		# 	elif num==2:
		# 		set_level="beta3"
		# 	elif num==3:
		# 		set_level="beta4"
		# 	elif num==4:
		# 		set_level="beta5"
		# 	p=marks_data(reference_id=set_id,group=get_group,current_round='First-Round',level=set_level,center='MPE KOTA',marks_first=float(i),time_first=5.0)
		# 	p.save()
		# 	set_id+=1
		# for i in range(1,int(max_semi)):
		# 	num=random.randint(0,4)
		# 	set_alpha_level(num)
		# 	set_level=""
		# 	if num==0:
		# 		set_level="beta1"
		# 	elif num==1:
		# 		set_level="beta2"
		# 	elif num==2:
		# 		set_level="beta3"
		# 	elif num==3:
		# 		set_level="beta4"
		# 	elif num==4:
		# 		set_level="beta5"
		# 	p=marks_data(reference_id=set_id,group=get_group,current_round='Semi-Finals',level=set_level,center='MPE KOTA',marks_semi=float(i),time_semi=5.0)
		# 	p.save()
		# 	set_id+=1
	# if get_group=="alpha":
		# for i in range(1,int(max_first)):
		# 	num=random.randint(0,1)
		# 	set_level=""
		# 	if num==0:	
		# 		set_level="alpha1"
		# 	elif num==1:
		# 		set_level="alpha2"
		# 	p=marks_data(reference_id=set_id,group=get_group,current_round='First-Round',level=set_level,center='MPE KOTA',marks_first=float(i),time_first=10.0)
		# 	p.save()
		# 	set_id+=1
		# for i in range(1,int(max_semi)):
		# 	num=random.randint(0,1)
		# 	set_alpha_level(num)
		# 	set_level=""
		# 	if num==0:	
		# 		set_level="alpha1"
		# 	elif num==1:
		# 		set_level="alpha2"
		# 	p=marks_data(reference_id=set_id,group=get_group,current_round='Semi-Finals',level=set_level,center='MPE KOTA',marks_semi=float(i),time_semi=10.0)
		# 	p.save()
		# 	set_id+=

def generate_marks(request):
	try:
		#generate(57.0,66.0,"thetha")
		return JsonResponse({'success':True})
	except Exception,e:
		return JsonResponse({'success':False},e)
		print e

@csrf_exempt
def send_email(request):
	if(request.method=="GET"):
		#return HttpResponseRedirect('/email/get_content.html')
		return render(request,"email/get_content.html")
	json={}
	data={}
	json['BASE_DIR']=str(request.scheme+"://"+request.get_host())
	attach_file=""
	if(request.method=="POST"):
		try:
			email_to=str(request.POST.get('email_to'))
			print email_to
			email_msg_head=str(request.POST.get('email_msg_head'))
			print email_msg_head
			email_msg=str(request.POST.get('email_msg'))
			email_msg= email_msg.replace("newline","\n")
			print email_msg
			data['msg']=email_msg
			data['msg_head']=email_msg_head
			verify_img=0
			try:
				image=request.FILES.get('pic').name
				print str(image)
				attach_file='/media/email_images/'+image
				folder = 'media/email_images/'
				print "image=",image
				fout = open(folder+image, 'w')
				file_content = request.FILES.get('pic').read()
				fout.write(file_content)
				fout.close()
			except Exception,e:
				verify_img=1
				print "Exception on Image",e
			try:
				#===========================Send Email===========================
				from_email = 'noreplycodenicely@gmail.com'
				template = get_template('email/email_content.html')
				path=str(request.scheme+"://"+request.get_host())
				print path
				text_content = 'This is an important message.'
				msg = EmailMultiAlternatives(email_msg_head, text_content, from_email, [email_to])
				data['url_path']=path
				html_content  = template.render(RequestContext(request,data,))
				msg.attach_alternative(html_content, "text/html")
				msg.mixed_subtype='related'
				if verify_img==0:
					for f in [attach_file]:
						fp = open(BASE_DIR+f, 'rb')
						msg_img = MIMEImage(fp.read())
						fp.close()
						msg_img.add_header('Content-ID', "inline".format(f), filename=str(image))
						msg.attach(msg_img)
				msg.send()
				print "Email Sent"
				#================================================================
			except Exception,e:
				image='image'
				print e
			#return JsonResponse({'success':True})
			return render(request,"email/email_content.html",data)
		except Exception,e:
			print e
			return HttpResponse("Email not Sent")

def register_raj(request):
	with open('raj_reg_data.json') as data_file:
		data = json.load(data_file)
		print data
	for o in data:
		try:
			print 'refrence_id',o['refrence_id']
			print 'first_name',o['firstname']
			try:
				b=user_data(refrence_id=o['refrence_id'],first_name=o['firstname'],last_name=o['lastname'],parent_father=o['fathername'],school=o['school'],email=o['email'],address=o['address'],number=o['number'],grade=o['grade'],exam_centre_1=o['exam_center_1'],exam_centre_2=o['exam_centre_2'],exam_group_1=o['exam_group_1'],exam_group_2=o['exam_group_2'],flag_exam_group_1=o['flag_exam_group_1'],flag_exam_group_2=o['flag_exam_group_2'],flag_workshop=o['flag_workshop'])
				b.save()
				print 'Done for Reference id - '+str(o['refrence_id'])
			except Exception,e:
				print 'Exception for Reference id - '+str(o['refrence_id']),e
		except Exception,e:
			print e
			print 'Exception for Reference id - '+str(o['refrence_id']),e

	#==============Updating Temporary Reference id to new generated Reference id =========================== 
	#========================= For Rajnandgaon Only--- in Marks Data========================================
	with open('raj_id_data.json') as data_file:
		data = json.load(data_file)
		print data
	for o in data:
		try:
			print '\nOld reference_id = ',o['reference_id_old']
			print 'New reference_id = ',o['reference_id_new']
			try:
				marks_details=marks_data.objects.get(reference_id=o['reference_id_old'])
				marks_details.reference_id=o['reference_id_new']
				marks_details.save()
				print 'Done for Reference id - '+str(o['reference_id_old'])
			except Exception,e:
				print 'Exception for Reference id - '+str(o['reference_id_old']),e
		except Exception,e:
			print e
			print 'Exception for Reference id - '+str(o['reference_id_old']),e

	# #==============Updating Temporary Reference id to new generated Reference id =========================== 
	# #========================= For Rajnandgaon Only----in Rank_data=========================================
	with open('raj_id_data.json') as data_file:
		data = json.load(data_file)
		print data
	for o in data:
		try:
			print '\nOld reference_id = ',o['reference_id_old']
			print 'New reference_id = ',o['reference_id_new']
			try:
				rank_details=rank_data.objects.get(reference_id=o['reference_id_old'])
				rank_details.reference_id=o['reference_id_new']
				rank_details.save()
				print 'Done for Reference id - '+str(o['reference_id_old'])
			except Exception,e:
				print 'Exception for Reference id - '+str(o['reference_id_old']),e
		except Exception,e:
			print e
			print 'Exception for Reference id - '+str(o['reference_id_old']),e
	return JsonResponse({})

def data_panel_login(request):
	if(request.method=="GET"):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/data_panel_home/')
		else:
			return render(request,'data_panel/panel_login.html')
		
	if(request.method=="POST"):
		username=str(request.POST.get('username'))
		password=str(request.POST.get('password'))
		print username
		print password
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			print "Authenticated"
			return HttpResponseRedirect('/data_panel_home/')
		else:
			print "Wrong username or password"
			return render(request,'data_panel/panel_login.html',{"invalid":True})

@login_required
def data_panel_logout(request):
    logout(request)
    return HttpResponseRedirect('/data_panel')


def data_panel_home(request):
	if(request.method=="GET"):
		if request.user.is_authenticated():
			return render(request,'data_panel/panel_home.html')
		else:
			return HttpResponseRedirect('/data_panel')
	if (request.method=="POST"):
		if 'admin_results' in request.POST:
			print "Redirect to admin result"
			return HttpResponseRedirect('/admin_results')
		elif 'national_level_rank' in request.POST:
			print "Redirect to national_all_rank_levelwise"
			return HttpResponseRedirect('/national_all_rank_levelwise')
		elif 'national_group_rank' in request.POST:
			print "Redirect to national_all_rank_groupwise"
			return HttpResponseRedirect('/national_all_rank_groupwise')
		elif 'spr_report' in request.POST:
			print "Redirect to spr_report"
			return HttpResponseRedirect('/spr_report')
		elif 'send_spr_report' in request.POST:
			print "Redirect to spr_report"
			return HttpResponseRedirect('/send_spr_panel')
		elif 'download_spr_report' in request.POST:
			print "Redirect for Download spr_report"
			return HttpResponseRedirect('/download_spr_panel')

@csrf_exempt
def send_spr_panel(request):
	if(request.method=="GET"):
		if request.user.is_authenticated():
			return render(request,'data_panel/panel_send_spr.html')
		else:
			return HttpResponseRedirect('/data_panel')

	if (request.method=="POST"):
		get_centre=str(request.POST.get('centre'))
		print get_centre
		get_group=str(request.POST.get('group'))
		print get_group		
		url_path=str(request.scheme+"://"+request.get_host())
		print url_path
		get_result=convert_to_pdf(request,get_centre,get_group,url_path)
		if get_result=="success":
			result="Email has been Sent."	
		elif get_result=="failure":
			result="No Data Availbale."
		else:
			result="Exception Occured."
		return render(request,'data_panel/panel_send_spr.html',{"done":True,"result":result})

@csrf_exempt
def download_spr_panel(request):
	if(request.method=="GET"):
		if request.user.is_authenticated():
			return render(request,'data_panel/panel_send_spr.html')
		else:
			return HttpResponseRedirect('/data_panel')

	if (request.method=="POST"):
		get_centre=str(request.POST.get('centre'))
		print get_centre
		get_group=str(request.POST.get('group'))
		print get_group		
		url_path=str(request.scheme+"://"+request.get_host())
		print url_path
		get_result=download_spr_into_pc(request,get_centre,get_group,url_path)
		return get_result	

def admin_results(request):
	if request.user.is_authenticated():
		login_display='<li><a href="/logout">Logout</a></li>'
		login_display2=''
	
	else:
		login_display=''
		login_display2='<li class="tab col s3"><a target="_self" href="/login">Login</a></li>'
	
	if(request.method=="GET"):
		return render(request,'spr_report/spr_main.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})

	if(request.method=="POST"):
		get_centre=str(request.POST.get('centre'))
		print get_centre
		get_group=str(request.POST.get('group'))
		print get_group		
		if get_centre!="all":
			if get_group!="all":
				center_list=marks_data.objects.filter(center=get_centre).values_list('center').distinct()
				group_list=marks_data.objects.filter(center=get_centre,group=get_group).values_list('group').distinct()
			else:
				center_list=marks_data.objects.filter(center=get_centre).values_list('center').distinct()
				group_list=marks_data.objects.filter(center=get_centre).order_by().values_list('group').distinct()
		else:
			center_list=marks_data.objects.order_by().values_list('center').distinct()
		try :
			# group_list=marks_data.objects.order_by().values_list('group').distinct()
			# level_list=marks_data.objects.order_by().values_list('level').distinct()
			result_data=''
			for center in center_list:
				if get_centre=="all":
					if get_group!="all":
						group_list=marks_data.objects.filter(center=center[0],group=get_group).values_list('group').distinct()
					else:
						group_list=marks_data.objects.filter(center=center[0]).order_by().values_list('group').distinct()
				for group in group_list:
					count=1
					result_data+='<div class="row"><div class="col s12 m0 "></div><div class="col s12 m12"><div class="card white darken-1" background-color="#FFD700"><div class="card-content black-text"><ul class="collection with-header"><center><li class="collection-header"><h4>'
					result_data+='Rank List '
					result_data+=str(center[0])+' '
					result_data+=str(group[0])+' '
					result_data+='</h4></li></center><div class="responsive-table"><table id="table"><thead><tr><th id="th" data-field="Rank">Rank</th><th id="th" data-field="Id">Roll Number</th><th id="th" data-field="Id">Group-Level</th><th id="th" data-field="Id">NPI Score</th><th id="th" data-field="Id">Current Round</th><th id="th" data-field="Id">National Level Rank</th><th id="th" data-field="Id">National Group Rank</th><th id="th" data-field="Id">Name</th><th id="th" data-field="Id">Father</th><th id="th" data-field="Id">Email</th><th id="th" data-field="Id">School</th><th id="th" data-field="Id">Class</th><th id="th" data-field="Id">Awards</th></tr></thead>'
					result_data+='<tbody id="'+str(group[0])+'">'
					print group[0]
					for groups_data in marks_data.objects.filter(Q(current_round='Finals') | Q(current_round='Semi-Finals') ,center=center[0],group=group[0]).order_by('-npi_semi'):
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
		except Exception,e:
			print "Exception : ",e
	try:
		return render(request,'spr_report/spr_main.html',{"result_data":result_data,"login_display":login_display,"login_display2":login_display2})

	except Exception,e:
		print e
		return render(request,'spr_report/spr_main.html',{"result_data":{},"login_display":login_display,"login_display2":login_display2})

def scheduler(request):
	# x=datetime.today()
	# y=x.replace(day=x.day+1, hour=16, minute=45, second=0, microsecond=0)
	# delta_t=y-x

	# secs=delta_t.seconds+1
	# #==================================
	# def hello_world():
	# 	print "hello world"
	# 	print "Time is ",datetime.today()
	# 	get_status=subprocess.call("sudo service mysql status",shell=True)
	# 	print get_status
	# 	print get_status.status
	# t = Timer(2, hello_world)
	# t.start()
	def repeat():
		def print_time():
			now=datetime.now()
			print "Date-Time = ",now.year, now.month, now.day, now.hour, now.minute
			new =now+timedelta(hours = 5,minutes=30)
			print "New Date-Time = ",new.year, new.month, new.day, new.hour, new.minute
			if new.hour==10:
				EmailMsg=EmailMessage("Hey!!! ","Good Morning. Have a nice day.",'bhirendra2014@gmail.com',['m3gh4l@gmail.com','bhirendra2014@gmail.com','shanu.rathi99@gmail.com'])
				EmailMsg.send()
				print "Email Sent"
			elif new.hour==14:
				EmailMsg=EmailMessage("Hey!!!! ","Good Afternoon.",'bhirendra2014@gmail.com',['m3gh4l@gmail.com','bhirendra2014@gmail.com','shanu.rathi99@gmail.com'])
				EmailMsg.send()
				print "Email Sent"
			elif new.hour==22:
				EmailMsg=EmailMessage("Hey!!!! ","Good Night.",'bhirendra2014@gmail.com',['m3gh4l@gmail.com','bhirendra2014@gmail.com','shanu.rathi99@gmail.com'])
				EmailMsg.send()
				print "Email Sent"
			s.enter(3600,1,print_time,argument=())
		s = sched.scheduler(time.time, time.sleep)
		s.enter(0,1,print_time,argument=())
		s.run()
	email_thread=threading.Thread(target=repeat,args=())
	email_thread.start()
	return HttpResponse({"success":True})
def mysql_status(request):
	def repeat():
		def sendMessage(print_status):
			msg = MIMEText("MySQL Status :-.\n" + print_status)
			subject = 'MySQL Status Report'
			EmailMsg=EmailMessage(subject,str(msg),'noreplycodenicely@gmail.com',['bhirendra2014@gmail.com','m3gh4l@gmail.com'])
			EmailMsg.send()
		print "Time is ",datetime.today()
		try:
			p = subprocess.Popen("service mysql status", stdout=subprocess.PIPE, shell=True) 
			get_status=p.communicate()[0]
			print get_status
		except Exception,e:
			print "Exception on command process :",e

		if "Active: active (running)" in get_status:
			print "Status : Running"
			#sendMessage("mysql is alive and running")
			s = sched.scheduler(time.time, time.sleep)
			delay_seconds = 3600
			s.enter(delay_seconds,1,repeat,argument=())
			s.run()
		else:
			print "Status : Failed"
			sendMessage("Failed")
			s = sched.scheduler(time.time, time.sleep)
			delay_seconds = 3600
			s.enter(delay_seconds,1,repeat,argument=())
			s.run()
	email_thread=threading.Thread(target=repeat,args=())
	email_thread.start()
	return HttpResponse({"success":True})

def dump_db(request):
	# try:
	# 	p = subprocess.Popen("chmod +x /root/dev/navmoweb/navmo/templates/data_panel/scripts/dump_db.py ; python /root/dev/navmoweb/navmo/templates/data_panel/scripts/dump_db.py", stdout=subprocess.PIPE, shell=True)
	# 	print "compiled file"
	# 	p.communicate()
	# 	# print "communication done--1"
	# 	# q = subprocess.Popen("python /root/dev/navmoweb/navmo/templates/data_panel/scripts/dump_db.py", stdout=subprocess.PIPE, shell=True)
	# 	# print "Script executed succesfully"
	# 	# get_status=q.communicate()
	# 	# print "communication done--2"
	# except Exception,e:
	# 	exc_type, exc_obj, exc_tb = sys.exc_info()
	# 	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	# 	print "Exception on Main Process :",e
	# 	print "Line no.= ",exc_tb.tb_lineno
	def repeat():
		def sendMessage():
			now=datetime.now()
			print "Date-Time = ",now.year, now.month, now.day, now.hour, now.minute
			new =now+timedelta(hours = 5,minutes=30)
			print "New Date-Time = ",new.year, new.month, new.day, new.hour, new.minute
			current_time=str(new.day)+"-"+str(new.month)+"-"+str(new.year)+"  "+str(new.hour)+":"+str(new.minute)
			FILE_NAME="sql_backup.sql"
			FILE_PATH=BASE_DIR+"/"+FILE_NAME
			print FILE_PATH
			msg = MIMEText("MySql Backup is Completed :\n\n sql file is attached.\n Backup Time is "+current_time)
			subject = 'MySQL Database Backup'
			EmailMsg=EmailMessage(subject,str(msg),'noreplycodenicely@gmail.com',['bhirendra2014@gmail.com','m3gh4l@gmail.com'])
			EmailMsg.attach_file(FILE_PATH)
			EmailMsg.send()
			print "Email Sent"
		print "Time is ",datetime.today()
		try:
			p = subprocess.Popen("mysqldump -u root -pLocalcart@999123 navmo > sql_backup.sql", stdout=subprocess.PIPE, shell=True) 
			p.communicate()
			sendMessage()  # Send backup sql file through email
			print "1st command worked"
			# q = subprocess.Popen("rm sql_backup.sql", stdout=subprocess.PIPE, shell=True) 
			# q.communicate()  # now remove the file from the folder
			# print "2nd command done"
			s = sched.scheduler(time.time, time.sleep)
			delay_seconds = 86400
			s.enter(delay_seconds,1,repeat,argument=())
			s.run()
		except Exception,e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print "Exception on command process :",e
			print "Line no.= ",exc_tb.tb_lineno
	email_thread=threading.Thread(target=repeat,args=())
	email_thread.start()	
	return HttpResponse({"success":True})

def graphs(request):
	data=[]
	count=0
	def put_point(ref_id,level):
		if str(ref_id)=="1600198":
			element.append(ref_id)
			element.append('Your Point for level '+level)
		else:
			element.append(None)
			element.append(None)
	for marks_details in marks_data.objects.order_by('-marks_first').order_by('time_first'):
		element=[]
		if marks_details.current_round=="Finals":
			if marks_details.time_final!=0.0:
				element.append(float(marks_details.time_first))
				element.append(float(marks_details.marks_first))
				try:	
					user_details=user_data.objects.get(refrence_id=marks_details.reference_id)
					put_point(user_details.refrence_id,marks_details.level)
				except Exception,e:
					element.append(None)
					element.append(None)
				data.append(element)
				count+=1
		elif marks_details.current_round=="Semi-Finals":
			if marks_details.time_semi!=0.0:
				element.append(float(marks_details.time_first))
				element.append(float(marks_details.marks_first))
				try:	
					user_details=user_data.objects.get(refrence_id=marks_details.reference_id)
					put_point(user_details.refrence_id,marks_details.level)
				except Exception,e:
					element.append(None)
					element.append(None)
				data.append(element)
				count+=1
		if marks_details.current_round=="First-Round":
			if marks_details.time_first!=0.0:
				element.append(float(marks_details.time_first))
				element.append(float(marks_details.marks_first))
				try:	
					user_details=user_data.objects.get(refrence_id=marks_details.reference_id)
					put_point(user_details.refrence_id,marks_details.level)
				except Exception,e:
					element.append(None)
					element.append(None)
				data.append(element)
				count+=1
	#print json.dumps(data)
	print "Total = ",count
	return render(request,"data_panel/graph1.html",{"data":json.dumps(data)})
	# data=[]
	# data.append(['Student','Time','Marks'])
	# count=0
	# for marks_details in marks_data.objects.filter(level="alpha1").order_by('-marks_first'):
	# 	element=[]
	# 	if marks_details.current_round=="Finals":
	# 		if marks_details.time_final!=0.0:
	# 			try:
	# 				user_details=user_data.objects.get(refrence_id=marks_details.reference_id)
	# 				element.append(str(marks_details.reference_id)+"("+user_details.first_name+")")
	# 				# element.append(marks_details.reference_id)
	# 			except Exception,e:
	# 				element.append(marks_details.reference_id)
	# 				print e
	# 			element.append(float(marks_details.time_first))
	# 			element.append(float(marks_details.marks_first))
	# 			data.append(element)
	# 			count+=1
	# 	elif marks_details.current_round=="Semi-Finals":
	# 		if marks_details.time_semi!=0.0:
	# 			try:
	# 				user_details=user_data.objects.get(refrence_id=marks_details.reference_id)
	# 				element.append(str(marks_details.reference_id)+"("+user_details.first_name+")")
	# 				# element.append(marks_details.reference_id)
	# 			except Exception,e:
	# 				element.append(marks_details.reference_id)
	# 				print e
	# 			element.append(float(marks_details.time_first))
	# 			element.append(float(marks_details.marks_first))
	# 			data.append(element)
	# 			count+=1
	# 	if marks_details.current_round=="First-Round":
	# 		if marks_details.time_first!=0.0:
	# 			try:
	# 				user_details=user_data.objects.get(refrence_id=marks_details.reference_id)
	# 				element.append(str(marks_details.reference_id)+"("+user_details.first_name+")")
	# 				# element.append(marks_details.reference_id)
	# 			except Exception,e:
	# 				element.append(marks_details.reference_id)
	# 				print e
	# 			element.append(float(marks_details.time_first))
	# 			element.append(float(marks_details.marks_first))
	# 			data.append(element)
	# 			count+=1
	# print data
	# print "Total = ",count
	# return render(request,"data_panel/graph2.html",{"data1":json.dumps(data)})
