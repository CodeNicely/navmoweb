from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# Create your views here.
@csrf_protect
def admit_card1(request):
# Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admit_demo.pdf"'

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    p.drawImage( 'media/admit_card_base.jpg', 0,500, width=585,height=343,mask=None) 
    p.drawImage( 'media/1600128/j2.jpg', 488,688, width=66,height=86,mask=None) 
    
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
    p.drawString(190, 653, "Exam Date")
    p.drawString(300, 653, "Exam Center")


    p.setFont("Vera", 8)

    p.drawString(120, 773, "1600016")    
    p.drawString(120, 763, "Meghal Agrawal")
    p.drawString(120, 753, "Anil Agrawal")
    p.drawString(120, 743, "Ritu Agrawal")
    p.drawString(120, 733, "5")
    p.drawString(120, 723, "Maharshi Vidya Mandir")
    p.drawString(120, 713, "Date of Birth")
    p.drawString(120, 703, "Gender")

    p.drawString(30, 630, "Beta Level 1 Abacus")
    p.drawString(190, 630, "13th Nov 2016")
    p.drawString(300, 630, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")

    p.drawString(30, 570, "Gamma MM 1")
    p.drawString(190, 570, "21st December 2016")
    p.drawString(300, 570, "HOLY CROSS SENIOR SECONDARY SCHOOL KAPA RAIPUR")


    # p.drawString(116, 753, "Anil Agrawal")
    # p.drawString(116, 743, "Anil Agrawal")
    # p.drawString(116, 733, "Anil Agrawal")
    # p.drawString(116, 723, "Anil Agrawal")
    # p.drawString(116, 713, "Anil Agrawal")
    # # Close the PDF object cleanly, and we're done.
    p.showPage()
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