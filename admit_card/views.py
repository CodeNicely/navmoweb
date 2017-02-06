from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from payment.models import payment_data
# Create your views here.
from .models import *
from register.models import user_data
from django.views.decorators.csrf import csrf_exempt
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

@csrf_exempt
def final_admit_card(request):
    try:
        refrence_id=request.GET.get('reference_id')
        print refrence_id
        admit_card_details=admit_card_data.objects.get(refrence_id=refrence_id)
        admit_card_details.date='14-01-2017'
        admit_card_details.time='11.00 AM'
        admit_card_details.center='Symbiosis International School, Gate No. 3, Symbiosis Viman Nagar Campus, Off., New Airport Rd, Viman Nagar'
        admit_card_details.city='Pune,    Maharashtra 411014'
        admit_card_details.save()
        second_round_admit_card_details=second_round_admit_card_data.objects.get(refrence_id=refrence_id)
        second_round_admit_card_details.current_round='Finals'
        return JsonResponse({"success":True})
    except Exception,e:
        print e
        return JsonResponse({"success":False,"message":str(e)})

#############################################################################################

@login_required
def admit_card1(request):
    refrence_id=str(request.user)
    user_data_row=user_data.objects.get(refrence_id=str(refrence_id))
    email=str(user_data_row.email)
    print email
    flag=payment_data.objects.get(refrence_id=str(refrence_id)).flag
    try:
        admit_card_row=admit_card_data.objects.get(refrence_id=str(refrence_id))
        title='NAVMO ADMIT CARD 2016-17'
        try:
            print 'Its for Round 2'
            second_round_admit_card_row=second_round_admit_card_data.objects.get(refrence_id=str(refrence_id))
            print 'Its for Round 2'
            
            if(flag==1):
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(refrence_id)+'.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."

                o=user_data_row
                o2=second_round_admit_card_row
                # buffer=StringIO()
                p = canvas.Canvas(response)
                
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 and o2.gamma_group_one==True and o2.alpha_beta_theta_group_two==True:
                    p.drawImage( 'media/admit_card_base.jpg', 0,323, width=585,height=520,mask=None) 
                else:
                    p.drawImage( 'media/admit_card_base_small.jpg', 0,398, width=585,height=442,mask=None) 


                try:
                    image_link=str(o.image.url)[1:]
                    print image_link
                    image_link1=image_link.replace(" ","")
                    print image_link1
                    p.drawImage(image_link1, 488,688, width=66,height=84,mask=None) 
                    print image_link1
                except Exception,e:
                    print e

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, title)
                if second_round_admit_card_row.current_round=='Semi-Finals':
                    p.drawString(240, 790, 'SEMI - FINALS')                    
                else:
                    p.drawString(284, 790, 'FINALS')
                    p.setFont("Vera", 8)
                    p.setFillColorRGB(255,0,0)
                    p.drawString(188, 600, "*Reporting time 10:00 AM")
                    p.setFillColorRGB(0,0,0)


                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Reference Id :")
                p.drawString(30, 763, "Name :")
                p.drawString(30, 753, "Father's Name :")
                p.drawString(30, 743, "Mother's Name :")
                p.drawString(30, 733, "Class :")
                p.drawString(30, 723, "School Name :")
                p.drawString(30, 713, "Date of Birth :")
                p.drawString(30, 703, "Gender :")
                p.drawString(30, 653, "Exam Course/Level")
                p.drawString(190, 653, "Exam Date/Time")
                p.drawString(300, 653, "Exam Center")

                p.setFont("Vera", 8)

                # p.drawString(30, 653, "Reporting time 10:00 AM")


                # p.drawString(120, 773, "1600016")    
                # p.drawString(120, 763, "Meghal Agrawal")
                # p.drawString(120, 753, "Anil Agrawal")
                # p.drawString(120, 743, "Ritu Agrawal")
                # p.drawString(120, 733, "5")
                # p.drawString(120, 723, "Maharshi Vidya Mandir")
                # p.drawString(120, 713, "Date of Birth")
                # p.drawString(120, 703, "Gender")

                # p.drawString(30, 630, "Beta Level 1 Abacus")
                # p.drawString(190, 630, "13th Nov 2016")
                # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                # p.drawString(30, 570, "Gamma MM 1")
                # p.drawString(190, 570, "21st December 2016")
                # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                p.setFont("Vera", 8)
                p.drawString(120, 773, o.refrence_id)#"1600016")    
                p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
                p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
                p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
                p.drawString(120, 733, o.grade)# "5")
                p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
                p.drawString(120, 713, o.dob)# "Date of Birth")
                p.drawString(120, 703, o.gender)# "Gender")
                ###########################################################################################################3##
                ####################################################################################################################
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 and o2.gamma_group_one==True and o2.alpha_beta_theta_group_two==True:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:59])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[59:116])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[116:174])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                    except Exception,e:
                        print e
                        pass
                    p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                    try:
                        p.drawString(30, 555, o.exam_group_2[30:60])
                        p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    
                    p.drawString(190, 570, admit_card_row.date)
                    p.drawString(190, 555, admit_card_row.time)
                
                    try:
                        p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:59]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[59:116]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[116:174]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass
                
                elif o.flag_exam_group_1==1 and o2.gamma_group_one==True:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:59])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[59:116])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[116:174])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass

                elif o.flag_exam_group_2==1 and o2.alpha_beta_theta_group_two==True:
                    p.drawString(30, 630, o.exam_group_2[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_2[30:60])
                        p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:59])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[59:116])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[116:174])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    except:
                        pass
                ##################################################################################################################333
                ################################################################################################################
                # p.drawString(116, 753, "Anil Agrawal")
                # p.drawString(116, 743, "Anil Agrawal")
                # p.drawString(116, 733, "Anil Agrawal")
                # p.drawString(116, 723, "Anil Agrawal")
                # p.drawString(116, 713, "Anil Agrawal")
                # # Close the PDF object cleanly, and we're done.
                #p.showPage()
                p.save()
                # pdf=buffer.getvalue()
                # buffer.close()
                # EmailMsg=EmailMessage("NAVMO 2016-17 Admit Card - "+str(refrence_id),"Here we are Attaching your Admit Card for NAVMO 2016-17 for Reference Id "+str(refrence_id),'noreplycodenicely@gmail.com',['contact@mindpowereducation.com','bhirendra2014@gmail.com','m3gh4l@gmail.com',str(o.email)])
                # EmailMsg.attach('admit_card_navmo'+str(refrence_id)+'.pdf',pdf,'application/pdf')
                # EmailMsg.send()
                # return HttpResponse("ok")
                return response

                # return response
            if flag==0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."
                # buffer=StringIO()
                p = canvas.Canvas(response)
            
                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Please confirm the payment first. We have not received your payment. ")
                p.drawString(30, 753, "For Queries Reach us at - contact@mindpowereducation.com")

                
                #p.showPage()
                p.save()
                # pdf = buffer.getvalue()
                # EmailMsg=EmailMessage("NAVMO 2016-17 Admit Card - "+str(refrence_id),"Here we are Attaching your Admit Card for NAVMO 2016-17 for Reference Id "+str(refrence_id),'noreplycodenicely@gmail.com',['contact@mindpowereducation.com','bhirendra2014@gmail.com','m3gh4l@gmail.com',str(o.email)])
                # EmailMsg.attach('admit_card_navmo'+str(refrence_id)+'.pdf',pdf,'application/pdf')
                # EmailMsg.send()
                print "Email Sent"


                # return HttpResponse("ok")
                return response

        except Exception,e:
            print 'Its for Round 1'
            print e

            title='NAVMO ADMIT CARD 2016-17'
            if(flag==1):
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(refrence_id)+'.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."

                o=user_data_row
                # buffer=StringIO()
                p = canvas.Canvas(response)
                # p = canvas.Canvas(response)
                
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 :
                    p.drawImage( 'media/admit_card_base.jpg', 0,323, width=585,height=520,mask=None) 
                else:
                    p.drawImage( 'media/admit_card_base_small.jpg', 0,398, width=585,height=442,mask=None) 


                try:
                    image_link=str(o.image.url)[1:]
                    print image_link
                    image_link1=image_link.replace(" ","")
                    print image_link1
                    p.drawImage( image_link1, 488,688, width=66,height=84,mask=None) 
                    print image_link1
                except Exception,e:
                    print e

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, title)
                p.drawString(240, 790, 'ROUND - 1')
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Reference Id :")
                p.drawString(30, 763, "Name :")
                p.drawString(30, 753, "Father's Name :")
                p.drawString(30, 743, "Mother's Name :")
                p.drawString(30, 733, "Class :")
                p.drawString(30, 723, "School Name :")
                p.drawString(30, 713, "Date of Birth :")
                p.drawString(30, 703, "Gender :")
                p.drawString(30, 653, "Exam Course/Level")
                p.drawString(190, 653, "Exam Date/Time")
                p.drawString(300, 653, "Exam Center")

                p.setFont("Vera", 8)
                p.drawString(30, 653, "Reporting time 10:00 AM")
                p.drawString(30, 623, "Reporting time 10:00 AM")


                # p.drawString(120, 773, "1600016")    
                # p.drawString(120, 763, "Meghal Agrawal")
                # p.drawString(120, 753, "Anil Agrawal")
                # p.drawString(120, 743, "Ritu Agrawal")
                # p.drawString(120, 733, "5")
                # p.drawString(120, 723, "Maharshi Vidya Mandir")
                # p.drawString(120, 713, "Date of Birth")
                # p.drawString(120, 703, "Gender")

                # p.drawString(30, 630, "Beta Level 1 Abacus")
                # p.drawString(190, 630, "13th Nov 2016")
                # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                # p.drawString(30, 570, "Gamma MM 1")
                # p.drawString(190, 570, "21st December 2016")
                # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                p.setFont("Vera", 8)
                p.drawString(120, 773, o.refrence_id)#"1600016")    
                p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
                p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
                p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
                p.drawString(120, 733, o.grade)# "5")
                p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
                p.drawString(120, 713, o.dob)# "Date of Birth")
                p.drawString(120, 703, o.gender)# "Gender")
                ###########################################################################################################3##
                ####################################################################################################################
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                    except Exception,e:
                        print e
                        pass
                    p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                    try:
                        p.drawString(30, 555, o.exam_group_2[30:60])
                        p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    
                    p.drawString(190, 570, admit_card_row.date)
                    p.drawString(190, 555, admit_card_row.time)
                
                    try:
                        p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:56]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[57:112]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[113:168]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass
                
                elif o.flag_exam_group_1==1:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass

                elif o.flag_exam_group_2==1:
                    p.drawString(30, 630, o.exam_group_2[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_2[30:60])
                        p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    except:
                        pass





                ##################################################################################################################333
                ################################################################################################################
                # p.drawString(116, 753, "Anil Agrawal")
                # p.drawString(116, 743, "Anil Agrawal")
                # p.drawString(116, 733, "Anil Agrawal")
                # p.drawString(116, 723, "Anil Agrawal")
                # p.drawString(116, 713, "Anil Agrawal")
                # # Close the PDF object cleanly, and we're done.
                #p.showPage()
                p.save()
                # pdf=buffer.getvalue()
                # EmailMsg=EmailMessage("NAVMO 2016-17 Admit Card - "+str(refrence_id),"Here we are Attaching your Admit Card for NAVMO 2016-17 for Reference Id "+str(refrence_id),'noreplycodenicely@gmail.com',['contact@mindpowereducation.com','bhirendra2014@gmail.com','m3gh4l@gmail.com',str(o.email)])
                # EmailMsg.attach('admit_card_navmo'+str(refrence_id)+'.pdf',pdf,'application/pdf')
                # EmailMsg.send()
                print "Email Sent"
                # return HttpResponse("ok")
                return response
                
            if flag==0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."
                # buffer=StringIO()
                p = canvas.Canvas(response)
            
                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Pls confirm the payment first")
                p.save()
                pdf=buffer.getvalue()
                EmailMsg=EmailMessage("NAVMO Admit Card - "+str(refrence_id),"Here we are Attaching your Admit Card for NAVMO 2016-17 for Reference Id "+str(refrence_id),'noreplycodenicely@gmail.com',['contact@mindpowereducation.com','bhirendra2014@gmail.com','m3gh4l@gmail.com',str(o.email)])
                EmailMsg.attach('admit_card_navmo'+str(refrence_id)+'.pdf',pdf,'application/pdf')
                EmailMsg.send()
                print "Email Sent"

                # return HttpResponse("ok")
                
                #p.showPage()
                p.save()
                return response

            print e

    except Exception,e:
        print e
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))

            # Create the PDF object, using the response object as its "file."
        # buffer=StringIO()
        p = canvas.Canvas(response)
        
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
        p.setFont("VeraBd", 12)
        p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
        p.setFont("VeraBd", 8)
        p.drawString(30, 773, "Admit cart hasnt been generated pls wait")
            
            #p.showPage()
        p.save()
        # pdf=buffer.getvalue()
        # EmailMsg=EmailMessage("Admit Card","Here we are Attaching your Admit Card for NAVMO 2016-17",'noreplycodenicely@gmail.com',['bhirendra2014@gmail.com','m3gh4l@gmail.com'])
        # EmailMsg.attach('yourChoosenFileName.pdf',pdf,'application/pdf')
        # EmailMsg.send()
        return response


############################################################################################################













@login_required
def admit_card1_old(request):
    user_data_row=user_data.objects.get(refrence_id=str(request.user))
    flag=payment_data.objects.get(refrence_id=str(request.user)).flag
    try:
        admit_card_row=admit_card_data.objects.get(refrence_id=str(request.user))
        title='NAVMO ADMIT CARD 2016-17'
        try:
            print 'Its for Round 2'
            second_round_admit_card_row=second_round_admit_card_data.objects.get(refrence_id=str(request.user))
            print 'Its for Round 2'
            
            if(flag==1):
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(request.user)+'.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."

                o=user_data_row
                o2=second_round_admit_card_row
                p = canvas.Canvas(response)
                
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 and o2.gamma_group_one==True and o2.alpha_beta_theta_group_two==True:
                    p.drawImage( 'media/admit_card_base.jpg', 0,323, width=585,height=520,mask=None) 
                else:
                    p.drawImage( 'media/admit_card_base_small.jpg', 0,398, width=585,height=442,mask=None) 


                try:
                    p.drawImage( str(o.image.url)[1:], 488,688, width=66,height=84,mask=None) 
                except Exception,e:
                    print e

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, title)
                p.drawString(240, 790, 'SEMI - FINALS')
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Reference Id :")
                p.drawString(30, 763, "Name :")
                p.drawString(30, 753, "Father's Name :")
                p.drawString(30, 743, "Mother's Name :")
                p.drawString(30, 733, "Class :")
                p.drawString(30, 723, "School Name :")
                p.drawString(30, 713, "Date of Birth :")
                p.drawString(30, 703, "Gender :")
                p.drawString(30, 653, "Exam Course/Level")
                p.drawString(190, 653, "Exam Date/Time")
                p.drawString(300, 653, "Exam Center")

                p.setFont("Vera", 8)

                # p.drawString(120, 773, "1600016")    
                # p.drawString(120, 763, "Meghal Agrawal")
                # p.drawString(120, 753, "Anil Agrawal")
                # p.drawString(120, 743, "Ritu Agrawal")
                # p.drawString(120, 733, "5")
                # p.drawString(120, 723, "Maharshi Vidya Mandir")
                # p.drawString(120, 713, "Date of Birth")
                # p.drawString(120, 703, "Gender")

                # p.drawString(30, 630, "Beta Level 1 Abacus")
                # p.drawString(190, 630, "13th Nov 2016")
                # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                # p.drawString(30, 570, "Gamma MM 1")
                # p.drawString(190, 570, "21st December 2016")
                # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                p.setFont("Vera", 8)
                p.drawString(120, 773, o.refrence_id)#"1600016")    
                p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
                p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
                p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
                p.drawString(120, 733, o.grade)# "5")
                p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
                p.drawString(120, 713, o.dob)# "Date of Birth")
                p.drawString(120, 703, o.gender)# "Gender")
                ###########################################################################################################3##
                ####################################################################################################################
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 and o2.gamma_group_one==True and o2.alpha_beta_theta_group_two==True:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                    except Exception,e:
                        print e
                        pass
                    p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                    try:
                        p.drawString(30, 555, o.exam_group_2[30:60])
                        p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    
                    p.drawString(190, 570, admit_card_row.date)
                    p.drawString(190, 555, admit_card_row.time)
                
                    try:
                        p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:56]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[57:112]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[113:168]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass
                
                elif o.flag_exam_group_1==1 and o2.gamma_group_one==True:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass

                elif o.flag_exam_group_2==1 and o2.alpha_beta_theta_group_two==True:
                    p.drawString(30, 630, o.exam_group_2[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_2[30:60])
                        p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    except:
                        pass
                ##################################################################################################################333
                ################################################################################################################
                # p.drawString(116, 753, "Anil Agrawal")
                # p.drawString(116, 743, "Anil Agrawal")
                # p.drawString(116, 733, "Anil Agrawal")
                # p.drawString(116, 723, "Anil Agrawal")
                # p.drawString(116, 713, "Anil Agrawal")
                # # Close the PDF object cleanly, and we're done.
                #p.showPage()
                p.save()
                return response
            if flag==0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response)
            
                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Please confirm the payment first. We have not received your payment. ")
                p.drawString(30, 753, "For Queries Reach us at - contact@mindpowereducation.com")

                
                #p.showPage()
                p.save()
                return response

        except Exception,e:
            print 'Its for Round 1'
            print e
            admit_card_row=admit_card_data.objects.get(refrence_id=str(request.user))
            refrence_id=request.user

            title='NAVMO ADMIT CARD 2016-17'
            if(flag==1):
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(refrence_id)+'.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."

                o=user_data_row
                p = canvas.Canvas(response)
                
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 :
                    p.drawImage( 'media/admit_card_base.jpg', 0,323, width=585,height=520,mask=None) 
                else:
                    p.drawImage( 'media/admit_card_base_small.jpg', 0,398, width=585,height=442,mask=None) 

                try:
                    p.drawImage( str(o.image.url)[1:], 488,688, width=66,height=84,mask=None) 
                except Exception,e:
                    print e

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, title)
                p.drawString(240, 790, 'ROUND - 1')
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Reference Id :")
                p.drawString(30, 763, "Name :")
                p.drawString(30, 753, "Father's Name :")
                p.drawString(30, 743, "Mother's Name :")
                p.drawString(30, 733, "Class :")
                p.drawString(30, 723, "School Name :")
                p.drawString(30, 713, "Date of Birth :")
                p.drawString(30, 703, "Gender :")
                p.drawString(30, 653, "Exam Course/Level")
                p.drawString(190, 653, "Exam Date/Time")
                p.drawString(300, 653, "Exam Center")

                p.setFont("Vera", 8)

                # p.drawString(120, 773, "1600016")    
                # p.drawString(120, 763, "Meghal Agrawal")
                # p.drawString(120, 753, "Anil Agrawal")
                # p.drawString(120, 743, "Ritu Agrawal")
                # p.drawString(120, 733, "5")
                # p.drawString(120, 723, "Maharshi Vidya Mandir")
                # p.drawString(120, 713, "Date of Birth")
                # p.drawString(120, 703, "Gender")

                # p.drawString(30, 630, "Beta Level 1 Abacus")
                # p.drawString(190, 630, "13th Nov 2016")
                # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                # p.drawString(30, 570, "Gamma MM 1")
                # p.drawString(190, 570, "21st December 2016")
                # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                p.setFont("Vera", 8)
                p.drawString(120, 773, o.refrence_id)#"1600016")    
                p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
                p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
                p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
                p.drawString(120, 733, o.grade)# "5")
                p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
                p.drawString(120, 713, o.dob)# "Date of Birth")
                p.drawString(120, 703, o.gender)# "Gender")
                ###########################################################################################################3##
                ####################################################################################################################
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                    except Exception,e:
                        print e
                        pass
                    p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                    try:
                        p.drawString(30, 555, o.exam_group_2[30:60])
                        p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    
                    p.drawString(190, 570, admit_card_row.date)
                    p.drawString(190, 555, admit_card_row.time)
                
                    try:
                        p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:56]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[57:112]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[113:168]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass
                
                elif o.flag_exam_group_1==1:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass

                elif o.flag_exam_group_2==1:
                    p.drawString(30, 630, o.exam_group_2[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_2[30:60])
                        p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    except:
                        pass





                ##################################################################################################################333
                ################################################################################################################
                # p.drawString(116, 753, "Anil Agrawal")
                # p.drawString(116, 743, "Anil Agrawal")
                # p.drawString(116, 733, "Anil Agrawal")
                # p.drawString(116, 723, "Anil Agrawal")
                # p.drawString(116, 713, "Anil Agrawal")
                # # Close the PDF object cleanly, and we're done.
                #p.showPage()
                p.save()
                return response
            if flag==0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response)
            
                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Pls confirm the payment first")
                
                #p.showPage()
                p.save()
                return response

            print e

    except Exception,e:
        print e
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
            # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)
        
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
        p.setFont("VeraBd", 12)
        p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
        p.setFont("VeraBd", 8)
        p.drawString(30, 773, "Admit cart hasnt been generated pls wait")
            
            #p.showPage()
        p.save()
        return response


@csrf_exempt
def admit_card_offline(request):
    refrence_id=request.GET.get('refid')
    user_data_row=user_data.objects.get(refrence_id=str(refrence_id))
    flag=payment_data.objects.get(refrence_id=str(refrence_id)).flag
    try:
        admit_card_row=admit_card_data.objects.get(refrence_id=str(refrence_id))
        title='NAVMO ADMIT CARD 2016-17'
        try:
            print 'Its for Round 2'
            second_round_admit_card_row=second_round_admit_card_data.objects.get(refrence_id=str(refrence_id))
            print 'Its for Round 2'
            
            if(flag==1):
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(refrence_id)+'.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."

                o=user_data_row
                o2=second_round_admit_card_row
                p = canvas.Canvas(response)
                
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 and o2.gamma_group_one==True and o2.alpha_beta_theta_group_two==True:
                    p.drawImage( 'media/admit_card_base.jpg', 0,323, width=585,height=520,mask=None) 
                else:
                    p.drawImage( 'media/admit_card_base_small.jpg', 0,398, width=585,height=442,mask=None) 


                try:
                    image_link=str(o.image.url)[1:]
                    print image_link
                    image_link1=image_link.replace(" ","")
                    print image_link1
                    p.drawImage(image_link1, 488,688, width=66,height=84,mask=None) 
                    print image_link1
                except Exception,e:
                    print e

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, title)
                p.drawString(240, 790, 'SEMI - FINALS')
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Reference Id :")
                p.drawString(30, 763, "Name :")
                p.drawString(30, 753, "Father's Name :")
                p.drawString(30, 743, "Mother's Name :")
                p.drawString(30, 733, "Class :")
                p.drawString(30, 723, "School Name :")
                p.drawString(30, 713, "Date of Birth :")
                p.drawString(30, 703, "Gender :")
                p.drawString(30, 653, "Exam Course/Level")
                p.drawString(190, 653, "Exam Date/Time")
                p.drawString(300, 653, "Exam Center")

                p.setFont("Vera", 8)

                # p.drawString(120, 773, "1600016")    
                # p.drawString(120, 763, "Meghal Agrawal")
                # p.drawString(120, 753, "Anil Agrawal")
                # p.drawString(120, 743, "Ritu Agrawal")
                # p.drawString(120, 733, "5")
                # p.drawString(120, 723, "Maharshi Vidya Mandir")
                # p.drawString(120, 713, "Date of Birth")
                # p.drawString(120, 703, "Gender")

                # p.drawString(30, 630, "Beta Level 1 Abacus")
                # p.drawString(190, 630, "13th Nov 2016")
                # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                # p.drawString(30, 570, "Gamma MM 1")
                # p.drawString(190, 570, "21st December 2016")
                # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                p.setFont("Vera", 8)
                p.drawString(120, 773, o.refrence_id)#"1600016")    
                p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
                p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
                p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
                p.drawString(120, 733, o.grade)# "5")
                p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
                p.drawString(120, 713, o.dob)# "Date of Birth")
                p.drawString(120, 703, o.gender)# "Gender")
                ###########################################################################################################3##
                ####################################################################################################################
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 and o2.gamma_group_one==True and o2.alpha_beta_theta_group_two==True:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                    except Exception,e:
                        print e
                        pass
                    p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                    try:
                        p.drawString(30, 555, o.exam_group_2[30:60])
                        p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    
                    p.drawString(190, 570, admit_card_row.date)
                    p.drawString(190, 555, admit_card_row.time)
                
                    try:
                        p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:56]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[57:112]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[113:168]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass
                
                elif o.flag_exam_group_1==1 and o2.gamma_group_one==True:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass

                elif o.flag_exam_group_2==1 and o2.alpha_beta_theta_group_two==True:
                    p.drawString(30, 630, o.exam_group_2[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_2[30:60])
                        p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    except:
                        pass
                ##################################################################################################################333
                ################################################################################################################
                # p.drawString(116, 753, "Anil Agrawal")
                # p.drawString(116, 743, "Anil Agrawal")
                # p.drawString(116, 733, "Anil Agrawal")
                # p.drawString(116, 723, "Anil Agrawal")
                # p.drawString(116, 713, "Anil Agrawal")
                # # Close the PDF object cleanly, and we're done.
                #p.showPage()
                p.save()
                return response
            if flag==0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response)
            
                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Please confirm the payment first. We have not received your payment. ")
                p.drawString(30, 753, "For Queries Reach us at - contact@mindpowereducation.com")

                
                #p.showPage()
                p.save()
                return response

        except Exception,e:
            print 'Its for Round 1'
            print e

            title='NAVMO ADMIT CARD 2016-17'
            if(flag==1):
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(refrence_id)+'.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."

                o=user_data_row
                p = canvas.Canvas(response)
                
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 :
                    p.drawImage( 'media/admit_card_base.jpg', 0,323, width=585,height=520,mask=None) 
                else:
                    p.drawImage( 'media/admit_card_base_small.jpg', 0,398, width=585,height=442,mask=None) 


                try:
                    image_link=str(o.image.url)[1:]
                    print image_link
                    image_link1=image_link.replace(" ","")
                    print image_link1
                    p.drawImage( image_link1, 488,688, width=66,height=84,mask=None) 
                    print image_link1
                except Exception,e:
                    print e

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, title)
                p.drawString(240, 790, 'ROUND - 1')
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Reference Id :")
                p.drawString(30, 763, "Name :")
                p.drawString(30, 753, "Father's Name :")
                p.drawString(30, 743, "Mother's Name :")
                p.drawString(30, 733, "Class :")
                p.drawString(30, 723, "School Name :")
                p.drawString(30, 713, "Date of Birth :")
                p.drawString(30, 703, "Gender :")
                p.drawString(30, 653, "Exam Course/Level")
                p.drawString(190, 653, "Exam Date/Time")
                p.drawString(300, 653, "Exam Center")

                p.setFont("Vera", 8)

                # p.drawString(120, 773, "1600016")    
                # p.drawString(120, 763, "Meghal Agrawal")
                # p.drawString(120, 753, "Anil Agrawal")
                # p.drawString(120, 743, "Ritu Agrawal")
                # p.drawString(120, 733, "5")
                # p.drawString(120, 723, "Maharshi Vidya Mandir")
                # p.drawString(120, 713, "Date of Birth")
                # p.drawString(120, 703, "Gender")

                # p.drawString(30, 630, "Beta Level 1 Abacus")
                # p.drawString(190, 630, "13th Nov 2016")
                # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                # p.drawString(30, 570, "Gamma MM 1")
                # p.drawString(190, 570, "21st December 2016")
                # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                p.setFont("Vera", 8)
                p.drawString(120, 773, o.refrence_id)#"1600016")    
                p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
                p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
                p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
                p.drawString(120, 733, o.grade)# "5")
                p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
                p.drawString(120, 713, o.dob)# "Date of Birth")
                p.drawString(120, 703, o.gender)# "Gender")
                ###########################################################################################################3##
                ####################################################################################################################
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                    except Exception,e:
                        print e
                        pass
                    p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                    try:
                        p.drawString(30, 555, o.exam_group_2[30:60])
                        p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    
                    p.drawString(190, 570, admit_card_row.date)
                    p.drawString(190, 555, admit_card_row.time)
                
                    try:
                        p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:56]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[57:112]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[113:168]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass
                
                elif o.flag_exam_group_1==1:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass

                elif o.flag_exam_group_2==1:
                    p.drawString(30, 630, o.exam_group_2[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_2[30:60])
                        p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    except:
                        pass





                ##################################################################################################################333
                ################################################################################################################
                # p.drawString(116, 753, "Anil Agrawal")
                # p.drawString(116, 743, "Anil Agrawal")
                # p.drawString(116, 733, "Anil Agrawal")
                # p.drawString(116, 723, "Anil Agrawal")
                # p.drawString(116, 713, "Anil Agrawal")
                # # Close the PDF object cleanly, and we're done.
                #p.showPage()
                p.save()
                return response
            if flag==0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response)
            
                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Pls confirm the payment first")
                
                #p.showPage()
                p.save()
                return response

            print e

    except Exception,e:
        print e
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
            # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)
        
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
        p.setFont("VeraBd", 12)
        p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
        p.setFont("VeraBd", 8)
        p.drawString(30, 773, "Admit cart hasnt been generated pls wait")
            
            #p.showPage()
        p.save()
        return response

@csrf_exempt
def admit_card_offline3(request):
    refrence_id=request.GET.get('refid')
    user_data_row=user_data.objects.get(refrence_id=str(refrence_id))
    email=str(user_data_row.email)
    print email
    flag=payment_data.objects.get(refrence_id=str(refrence_id)).flag
    try:
        admit_card_row=admit_card_data.objects.get(refrence_id=str(refrence_id))
        title='NAVMO ADMIT CARD 2016-17'
        try:
            print 'Its for Round 2'
            second_round_admit_card_row=second_round_admit_card_data.objects.get(refrence_id=str(refrence_id))
            print 'Its for Round 2'
            
            if(flag==1):
                # response = HttpResponse(content_type='application/pdf')
                # response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(refrence_id)+'.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."

                o=user_data_row
                o2=second_round_admit_card_row
                buffer=StringIO()
                p = canvas.Canvas(buffer)
                
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 and o2.gamma_group_one==True and o2.alpha_beta_theta_group_two==True:
                    p.drawImage( 'media/admit_card_base.jpg', 0,323, width=585,height=520,mask=None) 
                else:
                    p.drawImage( 'media/admit_card_base_small.jpg', 0,398, width=585,height=442,mask=None) 


                try:
                    image_link=str(o.image.url)[1:]
                    print image_link
                    image_link1=image_link.replace(" ","")
                    print image_link1
                    p.drawImage(image_link1, 488,688, width=66,height=84,mask=None) 
                    print image_link1
                except Exception,e:
                    print e

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, title)
                if second_round_admit_card_row.current_round=='Semi-Finals':
                    p.drawString(240, 790, 'SEMI - FINALS')                    
                else:
                    p.drawString(284, 790, 'FINALS')
                    p.setFont("Vera", 8)
                    p.setFillColorRGB(255,0,0)
                    p.drawString(188, 600, "*Reporting time 10:00 AM")
                    p.setFillColorRGB(0,0,0)


                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Reference Id :")
                p.drawString(30, 763, "Name :")
                p.drawString(30, 753, "Father's Name :")
                p.drawString(30, 743, "Mother's Name :")
                p.drawString(30, 733, "Class :")
                p.drawString(30, 723, "School Name :")
                p.drawString(30, 713, "Date of Birth :")
                p.drawString(30, 703, "Gender :")
                p.drawString(30, 653, "Exam Course/Level")
                p.drawString(190, 653, "Exam Date/Time")
                p.drawString(300, 653, "Exam Center")

                p.setFont("Vera", 8)

                # p.drawString(30, 653, "Reporting time 10:00 AM")


                # p.drawString(120, 773, "1600016")    
                # p.drawString(120, 763, "Meghal Agrawal")
                # p.drawString(120, 753, "Anil Agrawal")
                # p.drawString(120, 743, "Ritu Agrawal")
                # p.drawString(120, 733, "5")
                # p.drawString(120, 723, "Maharshi Vidya Mandir")
                # p.drawString(120, 713, "Date of Birth")
                # p.drawString(120, 703, "Gender")

                # p.drawString(30, 630, "Beta Level 1 Abacus")
                # p.drawString(190, 630, "13th Nov 2016")
                # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                # p.drawString(30, 570, "Gamma MM 1")
                # p.drawString(190, 570, "21st December 2016")
                # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                p.setFont("Vera", 8)
                p.drawString(120, 773, o.refrence_id)#"1600016")    
                p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
                p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
                p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
                p.drawString(120, 733, o.grade)# "5")
                p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
                p.drawString(120, 713, o.dob)# "Date of Birth")
                p.drawString(120, 703, o.gender)# "Gender")
                ###########################################################################################################3##
                ####################################################################################################################
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 and o2.gamma_group_one==True and o2.alpha_beta_theta_group_two==True:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:59])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[59:116])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[116:174])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                    except Exception,e:
                        print e
                        pass
                    p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                    try:
                        p.drawString(30, 555, o.exam_group_2[30:60])
                        p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    
                    p.drawString(190, 570, admit_card_row.date)
                    p.drawString(190, 555, admit_card_row.time)
                
                    try:
                        p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:59]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[59:116]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[116:174]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass
                
                elif o.flag_exam_group_1==1 and o2.gamma_group_one==True:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:59])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[59:116])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[116:174])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass

                elif o.flag_exam_group_2==1 and o2.alpha_beta_theta_group_two==True:
                    p.drawString(30, 630, o.exam_group_2[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_2[30:60])
                        p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:59])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[59:116])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[116:174])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    except:
                        pass
                ##################################################################################################################333
                ################################################################################################################
                # p.drawString(116, 753, "Anil Agrawal")
                # p.drawString(116, 743, "Anil Agrawal")
                # p.drawString(116, 733, "Anil Agrawal")
                # p.drawString(116, 723, "Anil Agrawal")
                # p.drawString(116, 713, "Anil Agrawal")
                # # Close the PDF object cleanly, and we're done.
                #p.showPage()
                p.save()
                pdf=buffer.getvalue()
                buffer.close()
                EmailMsg=EmailMessage("NAVMO 2016-17 Admit Card - "+str(refrence_id),"Here we are Attaching your Admit Card for NAVMO 2016-17 for Reference Id "+str(refrence_id),'noreplycodenicely@gmail.com',['contact@mindpowereducation.com','bhirendra2014@gmail.com','m3gh4l@gmail.com',str(o.email)])
                EmailMsg.attach('admit_card_navmo'+str(refrence_id)+'.pdf',pdf,'application/pdf')
                EmailMsg.send()
                return HttpResponse("ok")

                # return response
            if flag==0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."
                buffer=StringIO()
                p = canvas.Canvas(buffer)
            
                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Please confirm the payment first. We have not received your payment. ")
                p.drawString(30, 753, "For Queries Reach us at - contact@mindpowereducation.com")

                
                #p.showPage()
                p.save()
                pdf = buffer.getvalue()
                EmailMsg=EmailMessage("NAVMO 2016-17 Admit Card - "+str(refrence_id),"Here we are Attaching your Admit Card for NAVMO 2016-17 for Reference Id "+str(refrence_id),'noreplycodenicely@gmail.com',['contact@mindpowereducation.com','bhirendra2014@gmail.com','m3gh4l@gmail.com',str(o.email)])
                EmailMsg.attach('admit_card_navmo'+str(refrence_id)+'.pdf',pdf,'application/pdf')
                EmailMsg.send()
                print "Email Sent"


                return HttpResponse("ok")

        except Exception,e:
            print 'Its for Round 1'
            print e

            title='NAVMO ADMIT CARD 2016-17'
            if(flag==1):
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(refrence_id)+'.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."

                o=user_data_row
                buffer=StringIO()
                p = canvas.Canvas(buffer)
                # p = canvas.Canvas(response)
                
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 :
                    p.drawImage( 'media/admit_card_base.jpg', 0,323, width=585,height=520,mask=None) 
                else:
                    p.drawImage( 'media/admit_card_base_small.jpg', 0,398, width=585,height=442,mask=None) 


                try:
                    image_link=str(o.image.url)[1:]
                    print image_link
                    image_link1=image_link.replace(" ","")
                    print image_link1
                    p.drawImage( image_link1, 488,688, width=66,height=84,mask=None) 
                    print image_link1
                except Exception,e:
                    print e

                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, title)
                p.drawString(240, 790, 'ROUND - 1')
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Reference Id :")
                p.drawString(30, 763, "Name :")
                p.drawString(30, 753, "Father's Name :")
                p.drawString(30, 743, "Mother's Name :")
                p.drawString(30, 733, "Class :")
                p.drawString(30, 723, "School Name :")
                p.drawString(30, 713, "Date of Birth :")
                p.drawString(30, 703, "Gender :")
                p.drawString(30, 653, "Exam Course/Level")
                p.drawString(190, 653, "Exam Date/Time")
                p.drawString(300, 653, "Exam Center")

                p.setFont("Vera", 8)
                p.drawString(30, 653, "Reporting time 10:00 AM")
                p.drawString(30, 623, "Reporting time 10:00 AM")


                # p.drawString(120, 773, "1600016")    
                # p.drawString(120, 763, "Meghal Agrawal")
                # p.drawString(120, 753, "Anil Agrawal")
                # p.drawString(120, 743, "Ritu Agrawal")
                # p.drawString(120, 733, "5")
                # p.drawString(120, 723, "Maharshi Vidya Mandir")
                # p.drawString(120, 713, "Date of Birth")
                # p.drawString(120, 703, "Gender")

                # p.drawString(30, 630, "Beta Level 1 Abacus")
                # p.drawString(190, 630, "13th Nov 2016")
                # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                # p.drawString(30, 570, "Gamma MM 1")
                # p.drawString(190, 570, "21st December 2016")
                # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                p.setFont("Vera", 8)
                p.drawString(120, 773, o.refrence_id)#"1600016")    
                p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
                p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
                p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
                p.drawString(120, 733, o.grade)# "5")
                p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
                p.drawString(120, 713, o.dob)# "Date of Birth")
                p.drawString(120, 703, o.gender)# "Gender")
                ###########################################################################################################3##
                ####################################################################################################################
                if o.flag_exam_group_1==1 and o.flag_exam_group_2==1:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                    except Exception,e:
                        print e
                        pass
                    p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                    try:
                        p.drawString(30, 555, o.exam_group_2[30:60])
                        p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    
                    p.drawString(190, 570, admit_card_row.date)
                    p.drawString(190, 555, admit_card_row.time)
                
                    try:
                        p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:56]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[57:112]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[113:168]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass
                
                elif o.flag_exam_group_1==1:
                    p.drawString(30, 630, o.exam_group_1[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_1[30:60])
                        p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    
                    except:
                        pass

                elif o.flag_exam_group_2==1:
                    p.drawString(30, 630, o.exam_group_2[:30])
                    try:
                        p.drawString(30, 615, o.exam_group_2[30:60])
                        p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                    except:
                        pass
                    

                    p.drawString(190, 630, admit_card_row.date)
                    p.drawString(190, 615, admit_card_row.time)
                    try:
                        p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                        p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    except:
                        pass





                ##################################################################################################################333
                ################################################################################################################
                # p.drawString(116, 753, "Anil Agrawal")
                # p.drawString(116, 743, "Anil Agrawal")
                # p.drawString(116, 733, "Anil Agrawal")
                # p.drawString(116, 723, "Anil Agrawal")
                # p.drawString(116, 713, "Anil Agrawal")
                # # Close the PDF object cleanly, and we're done.
                #p.showPage()
                p.save()
                pdf=buffer.getvalue()
                EmailMsg=EmailMessage("NAVMO 2016-17 Admit Card - "+str(refrence_id),"Here we are Attaching your Admit Card for NAVMO 2016-17 for Reference Id "+str(refrence_id),'noreplycodenicely@gmail.com',['contact@mindpowereducation.com','bhirendra2014@gmail.com','m3gh4l@gmail.com',str(o.email)])
                EmailMsg.attach('admit_card_navmo'+str(refrence_id)+'.pdf',pdf,'application/pdf')
                EmailMsg.send()
                print "Email Sent"
                return HttpResponse("ok")
                
            if flag==0:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

                pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
                pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
                # Create the PDF object, using the response object as its "file."
                buffer=StringIO()
                p = canvas.Canvas(buffer)
            
                # Draw things on the PDF. Here's where the PDF generation happens.
                # See the ReportLab documentation for the full list of functionality.
                p.setFont("VeraBd", 12)
                p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
                p.setFont("VeraBd", 8)
                p.drawString(30, 773, "Pls confirm the payment first")
                p.save()
                pdf=buffer.getvalue()
                EmailMsg=EmailMessage("NAVMO Admit Card - "+str(refrence_id),"Here we are Attaching your Admit Card for NAVMO 2016-17 for Reference Id "+str(refrence_id),'noreplycodenicely@gmail.com',['contact@mindpowereducation.com','bhirendra2014@gmail.com','m3gh4l@gmail.com',str(o.email)])
                EmailMsg.attach('admit_card_navmo'+str(refrence_id)+'.pdf',pdf,'application/pdf')
                EmailMsg.send()
                print "Email Sent"

                return HttpResponse("ok")
                
                #p.showPage()
                # p.save()
                # return response

            print e

    except Exception,e:
        print e
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))

            # Create the PDF object, using the response object as its "file."
        buffer=StringIO()
        p = canvas.Canvas(buffer)
        
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
        p.setFont("VeraBd", 12)
        p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
        p.setFont("VeraBd", 8)
        p.drawString(30, 773, "Admit cart hasnt been generated pls wait")
            
            #p.showPage()
        p.save()
        # pdf=buffer.getvalue()
        # EmailMsg=EmailMessage("Admit Card","Here we are Attaching your Admit Card for NAVMO 2016-17",'noreplycodenicely@gmail.com',['bhirendra2014@gmail.com','m3gh4l@gmail.com'])
        # EmailMsg.attach('yourChoosenFileName.pdf',pdf,'application/pdf')
        # EmailMsg.send()
        return response


@csrf_exempt
def admit_card_offline1(request):

    refrence_id=request.GET.get('refid')
    user_data_row=user_data.objects.get(refrence_id=str(refrence_id))
    flag=payment_data.objects.get(refrence_id=str(refrence_id)).flag
    try:
        admit_card_row=admit_card_data.objects.get(refrence_id=str(refrence_id))
        if(flag==1):
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="admit_card_navmo'+str(refrence_id)+'.pdf"'

            pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
            pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
            # Create the PDF object, using the response object as its "file."

            o=user_data_row
            p = canvas.Canvas(response)
            
            if o.flag_exam_group_1==1 and o.flag_exam_group_2==1 :
                p.drawImage( 'media/admit_card_base.jpg', 0,500, width=585,height=343,mask=None) 
            else:
                p.drawImage( 'media/admit_card_base_small.jpg', 0,570, width=585,height=270,mask=None) 


            try:
                p.drawImage( str(o.image.url)[1:], 488,688, width=66,height=84,mask=None) 
            except Exception,e:
                print e

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.setFont("VeraBd", 12)
            p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
            p.setFont("VeraBd", 8)
            p.drawString(30, 773, "Reference Id :")
            p.drawString(30, 763, "Name :")
            p.drawString(30, 753, "Father's Name :")
            p.drawString(30, 743, "Mother's Name :")
            p.drawString(30, 733, "Class :")
            p.drawString(30, 723, "School Name :")
            p.drawString(30, 713, "Date of Birth :")
            p.drawString(30, 703, "Gender :")
            p.drawString(30, 653, "Exam Course/Level")
            p.drawString(190, 653, "Exam Date/Time")
            p.drawString(300, 653, "Exam Center")

            p.setFont("Vera", 8)

            # p.drawString(120, 773, "1600016")    
            # p.drawString(120, 763, "Meghal Agrawal")
            # p.drawString(120, 753, "Anil Agrawal")
            # p.drawString(120, 743, "Ritu Agrawal")
            # p.drawString(120, 733, "5")
            # p.drawString(120, 723, "Maharshi Vidya Mandir")
            # p.drawString(120, 713, "Date of Birth")
            # p.drawString(120, 703, "Gender")

            # p.drawString(30, 630, "Beta Level 1 Abacus")
            # p.drawString(190, 630, "13th Nov 2016")
            # p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

            # p.drawString(30, 570, "Gamma MM 1")
            # p.drawString(190, 570, "21st December 2016")
            # p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

            p.setFont("Vera", 8)
            p.drawString(120, 773, o.refrence_id)#"1600016")    
            p.drawString(120, 763, o.first_name+' '+o.last_name)#"Meghal Agrawal")
            p.drawString(120, 753, o.parent_father)# "Anil Agrawal")
            p.drawString(120, 743, o.parent_mother)# "Ritu Agrawal")
            p.drawString(120, 733, o.grade)# "5")
            p.drawString(120, 723, o.school[:70])# "Maharshi Vidya Mandir")
            p.drawString(120, 713, o.dob)# "Date of Birth")
            p.drawString(120, 703, o.gender)# "Gender")
            ###########################################################################################################3##
            ####################################################################################################################
            if o.flag_exam_group_1==1 and o.flag_exam_group_2==1:
                p.drawString(30, 630, o.exam_group_1[:30])
                try:
                    p.drawString(30, 615, o.exam_group_1[30:60])
                    p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                except:
                    pass
                

                p.drawString(190, 630, admit_card_row.date)
                p.drawString(190, 615, admit_card_row.time)
                
                try:
                    p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

                except Exception,e:
                    print e
                    pass
                p.drawString(30, 570, o.exam_group_2[:30])# "Gamma MM 1")
                try:
                    p.drawString(30, 555, o.exam_group_2[30:60])
                    p.drawString(30, 540, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                except:
                    pass
                
                p.drawString(190, 570, admit_card_row.date)
                p.drawString(190, 555, admit_card_row.time)
            
                try:
                    p.drawString(300, 570, str(admit_card_row.center+","+admit_card_row.city)[:56]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    p.drawString(300, 555, str(admit_card_row.center+","+admit_card_row.city)[57:112]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    p.drawString(300, 540, str(admit_card_row.center+","+admit_card_row.city)[113:168]) #"HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                
                except:
                    pass
            
            elif o.flag_exam_group_1==1:
                p.drawString(30, 630, o.exam_group_1[:30])
                try:
                    p.drawString(30, 615, o.exam_group_1[30:60])
                    p.drawString(30, 600, o.exam_group_1[60:90])# "Beta Level 1 Abacus")
                except:
                    pass
                

                p.drawString(190, 630, admit_card_row.date)
                p.drawString(190, 615, admit_card_row.time)
                try:
                    p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                
                except:
                    pass

            elif o.flag_exam_group_2==1:
                p.drawString(30, 630, o.exam_group_2[:30])
                try:
                    p.drawString(30, 615, o.exam_group_2[30:60])
                    p.drawString(30, 600, o.exam_group_2[60:90])# "Beta Level 1 Abacus")
                except:
                    pass
                

                p.drawString(190, 630, admit_card_row.date)
                p.drawString(190, 615, admit_card_row.time)
                try:
                    p.drawString(300, 630, str(admit_card_row.center+","+admit_card_row.city)[:56])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    p.drawString(300, 615, str(admit_card_row.center+","+admit_card_row.city)[57:112])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                    p.drawString(300, 600, str(admit_card_row.center+","+admit_card_row.city)[113:168])# "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")
                except:
                    pass





            ##################################################################################################################333
            ################################################################################################################
            # p.drawString(116, 753, "Anil Agrawal")
            # p.drawString(116, 743, "Anil Agrawal")
            # p.drawString(116, 733, "Anil Agrawal")
            # p.drawString(116, 723, "Anil Agrawal")
            # p.drawString(116, 713, "Anil Agrawal")
            # # Close the PDF object cleanly, and we're done.
            #p.showPage()
            p.save()
            return response
        if flag==0:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

            pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
            pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
            # Create the PDF object, using the response object as its "file."
            p = canvas.Canvas(response)
        
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.setFont("VeraBd", 12)
            p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
            p.setFont("VeraBd", 8)
            p.drawString(30, 773, "Pls confirm the payment first")
            
            #p.showPage()
            p.save()
            return response
    except Exception,e:
        print e
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
            # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)
        
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
        p.setFont("VeraBd", 12)
        p.drawString(200, 810, "NAVMO ADMIT CARD 2016-17")
        p.setFont("VeraBd", 8)
        p.drawString(30, 773, "Admit cart hasnt been generated pls wait")
            
            #p.showPage()
        p.save()
        return response


def admit_card(request):
	 # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 850, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@csrf_exempt
def send_email(request):
    try:



        html = """\
            <html>
            <title></title>
            <link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <!--Import materialize.css-->
        <link type="text/css" rel="stylesheet" href="http://www.mpenavmo.com/static/materialize/css/materialize.min.css"  media="screen,projection"/>
        <link type="text/css" rel="stylesheet" href="http://www.mpenavmo.com/static/materialize/css/colour.css"  media="screen,projection"/>

        <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
        <script type="text/javascript" src="http://www.mpenavmo.com/static/materialize/js/materialize.min.js"></script>

<style>
body {
    background-color:#424242;
}
</style>
            <body>

            <div class="card">
    <div class="card-image waves-effect waves-block waves-light">
      <center><img class="activator" height="240" width="240" src="http://www.mpenavmo.com/media/happy_new_year.gif"><center>
    </div>
    <div class="card-content">
      <span class="card-title activator grey-text text-darken-4">Card Title<i class="material-icons right">more_vert</i></span>
      <p><a href="#">This is a link</a></p>
    </div>
    <div class="card-reveal">
      <span class="card-title grey-text text-darken-4">Card Title<i class="material-icons right">close</i></span>
      <p>Here is some more information about this product that is only revealed once clicked on.</p>
    </div>
  </div>
            </body>
            </html>
            """
        html1 = """\
            <html>
            <head></head>
            <body>
            <p>Hi!<br>
            <h1>How are you?</h1><br>
            Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
            </body>
            </html>
            """
        

        part2 = MIMEText(html, 'html')
        message='<html><head><title>HTML email</title></head><body><p>This email contains HTML Tags!</p>'
        message+='<table><tr><th>Firstname</th><th>Lastname</th></tr><tr><td>John</td><td>Doe</td></tr></table></body></html>'
        EmailMsg=EmailMessage("Happy New Year 2017",'message','noreplycodenicely@gmail.com',['m3gh4l@gmail.com'])
        EmailMsg.attach(part2)
        EmailMsg.send()
        return JsonResponse({"success":True,"message":"Mail Sent Successfully"})
    except Exception,e:
        print e     
        return JsonResponse({"success":False,"message":e})

def release_admit_card(request):
    if request.method=='GET':
        try:
            second_round_admit_card_row=second_round_admit_card_data.objects.filter(current_round='Finals')
            i=1
            for o in second_round_admit_card_row:
               print i
               i+=1
               print o.refrence_id 
               url="http://mpenavmo.com:8989/admit_card_offline3?refid="+str(o.refrence_id)
               print requests.request('GET', url)
            return JsonResponse({"success":True})
        except Exception,e:
            print e
            return JsonResponse({"success":False,"message":str(e)})