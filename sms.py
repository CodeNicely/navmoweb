import requests
from register.models import keys_data
def send_sms(mobile_number,message,sender_id="mNavmo"):
	authkey=str(keys_data.objects.get(key="msg91").value)
	url='http://api.msg91.com/api/sendhttp.php?authkey='+authkey+'&mobiles='
	url+=mobile_number
	url+='&message='+message
	url+='&sender='+sender_id+'&route=4'
	print url
	print requests.request('GET', url)
