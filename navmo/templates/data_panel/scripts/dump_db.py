from django.core.mail import EmailMessage
import os
from datetime import datetime,timedelta
import threading
from threading import Timer
import sched, time,subprocess
from subprocess import Popen, PIPE, STDOUT
from email.mime.text import MIMEText
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def repeat():
	def sendMessage():
		now=datetime.now()
		print "Date-Time = ",now.year, now.month, now.day, now.hour, now.minute
		new =now+timedelta(hours = 5,minutes=30)
		print "New Date-Time = ",new.year, new.month, new.day, new.hour, new.minute
		current_time=new.day+"-"+new.month+"-"+new.year+"  "+new.hour+":"+new.minute
		FILE_NAME="sql_backup.sql"
		FILE_PATH=BASE_DIR+"/"+FILE_NAME
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
		q = subprocess.Popen("rm sql_backup.sql", stdout=subprocess.PIPE, shell=True) 
		q.communicate()  # now remove the file from the folder
		s = sched.scheduler(time.time, time.sleep)
		delay_seconds = 86400
		s.enter(delay_seconds,1,repeat,argument=())
		s.run()
	except Exception,e:
		print "Exception on command process :",e

email_thread=threading.Thread(target=repeat,args=())
email_thread.start()
# return HttpResponse({"success":True})