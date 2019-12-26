# -*- coding: utf-8 -*-
import netmiko
import string
import random
from mailer import send_mail
import os

ip = os.environ.get('mik_ip')
login = os.environ.get('mik_login')
password = os.environ.get('mik_pass')
port=os.environ.get('mik_port')
command=':wq!'


mail_message = '''
Hello, The Password of the Guest WIFI has been changed.
SSID: MBMFWF
Password: {}
'''

def generate_pass(length=8):
	'Generate password with the length'
	symbols=string.ascii_uppercase + string.ascii_lowercase + string.digits
	return ''.join(random.choices(symbols,k=length))

def mikrotik_change_passwd(new_pass,ip,login,password):
	pass

	
if __name__=="__main__":
	
	print(ip)	
