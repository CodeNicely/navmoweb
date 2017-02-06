from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.shortcuts import render_to_response, render
import json
# Create your views here.

def photo_gallery(request):
	if request.method=='GET':
		try:
			response_data={}
			if request.user.is_authenticated():
				login_display='<li><a href="/logout">Logout</a></li>'
				login_display2=''
			else:
				login_display=''
				login_display2='<li><a href="/login">Login</a></li>'
			
			photos_list=gallery_data.objects.all()
			image_list='<div class="row">'
			i=0
			for o in photos_list:
				
				image_list+='<div class="col s12 m3"><div class="card"><div class="card-image">'
				image_list+='<img src="'+str(o.image)[11:]+'"  >'
				image_list+='</div><div class="card-content">'+o.caption+'</div></div></div>'
				# image_list+='<div class="col s12 m3">'
				# image_list+='<img class="materialboxed" src="'+str(o.image)[11:]+'"  data-caption="'+o.caption+'" >'
				# image_list+='</div>'
			

			image_list+='</div>'
				# data['image']=str(o.image)
				# data['caption']=o.caption
			response_data['image_list']=image_list
			response_data['login_display']=login_display
			response_data['login_display2']=login_display2
			print response_data
			result_data=json.dumps(response_data)
			print result_data
			return render(request,'photo_gallery/photo_gallery.html',response_data)
		except Exception,e:
			print e
			return render(request,'photo_gallery/photo_gallery.html',{})
	else:
		return JsonResponse({"success":False,"message":"Get out of Here or We Will Hack your World! We the Developers Know your Ip here."})
