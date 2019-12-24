# -*- coding: utf-8 -*-
#import routeros_api
import string
import random
import smtplib
import routeros
from mailer import send_mail

mail_message = '''
Hello, The Password on the Guest WIFI has been changed.
SSID: MBMFWF
Password: {}
'''

def generate_pass(length=8):
	'Generate password with the length'
	symbols=string.ascii_uppercase + string.ascii_lowercase + string.digits
	return ''.join(random.choices(symbols,k=length))



	
if __name__=="__main__":
	print(generate_pass())	
