# -*- coding: utf-8 -*-
#!/bin/python3
import requests
import json
import netmiko
import string
import random
import os
import re
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from faker import Faker



ip = os.environ.get('mik_ip')
login = os.environ.get('mik_login')
password = os.environ.get('mik_pass')
port=os.environ.get('mik_port')
#command='/interface wireless security-profiles print detail value-list'
command='/interface wireless security-profiles print detail value-list'
mail_ip=os.environ.get('mail_ip')
mail_port=os.environ.get('mail_port')
mail_clients=os.environ.get('mail_clients')


logging.basicConfig(filename='wifi.log',filemode='w',level=logging.INFO)


success_message = '''
Hello, The Password of the Guest WIFI has been changed.
SSID: MBMFWF
New Password: {}
'''
error_message = '''
Hello.
	The error occured due to change the password on the Guest WIFI
Please check the log of the script.

'''





def send_mail(from_addr, to_addr, message_text, subject='No Subject',smtp_server_ip='203.59.72.37',smtp_port = '25', smtp_auth = False, smtp_login = None, smtp_pass = None, tls=False):
    '''The function is sending email notification '''
    msg = MIMEMultipart()
    msg['From']=from_addr
    msg['To']=','.join(to_addr)
    msg['Subject'] = subject
    body =  message_text
    #Creating a msg based on PLAIN text
    msg.attach(MIMEText(body,'plain'))
    #Convert msg to  the string
    text_msg = msg.as_string()

    #Sending a mail to the server
    smtp_server =  smtplib.SMTP(smtp_server_ip,smtp_port)
    #Testing the connection
    smtp_server.ehlo()
    if smtp_auth:
        smtp_server.login(smtp_login,smtp_pass)
        if tls:
            smtp.starttls()
    smtp_server.sendmail(from_addr,to_addr, text_msg)
    smtp_server.quit()

def send_rocket(rocket_webhook,new_password,channel_name,text_message,username="Rocket.Cat",avatar=":wifi:"):
    "Sends a notification to rocket channel"
    payload = {"username":"Rocket.Cat","icon_emoji":":wifi:","channel":channel_name}
    r = request.post(url,json.dump(payload))
    

class Mikrot:
    def __init__(self,login,password,ip,port=22):
        self.username=login
        self.password=password
        self.ip=ip
        self.port=port
        self.dev={'device_type':"mikrotik_routeros","username":self.username,"password":self.password,'ip':self.ip,'port':self.port}
        self._current_pass=None
        self._ex_pass=None
    @classmethod    
    def generate_pass(cls):
        'Generate password by using faker'
        fake = Faker()
        lst_pass = [fake.first_name() + fake.last_name() + fake.year() for i in range(100)]
        new_password = random.choice(lst_pass)
        logging.info(f'generating a new password: {new_password}')
        return new_password
    
    def show_command(self,command):
        logging.info(f'connecting to {self.ip} device to get the config')
        with netmiko.ConnectHandler(**self.dev) as ssh:
            result=ssh.send_command(command)
        logging.info(f'router config: \n {result}')
        return result

    def change_wifi_passwd(self,new_password):
        re_pat='passphrase=\"(\w+)\"'
        cmd_get_current_pass='/caps-man security print'
        #cmd_passwd_change=f'/caps-man security set security-profile passphrase={new_password}'
        cmd_passwd_change=f'/caps-man security set security1 passphrase={new_password}'
        raw_current_pass = self.show_command(cmd_get_current_pass)
        
        #try to connect and set up a new password
        try:
            with netmiko.ConnectHandler(**self.dev,default_enter="\n\r") as ssh:
                ssh.send_command(cmd_passwd_change.format(new_password))
        except:
            logging.warning(f'Unable to connect to {self.ip} to write a new password in the router')
            return False
        #parsing output from Mikrotik and searching current password.
        self._prev_pass=re.search(re_pat,raw_current_pass).group(1)
        self._current_pass=new_password
        logging.info(f'Password was successfully written to the router {self.ip}')
        return True
    
    @property
    def get_pass(self):
        return self._current_pass
    @property
    def get_expass(self):
        return self._ex_pass

def main_prog():
    myrouter=Mikrot(login=login,password=password,ip=ip,port=port)
    new_password=Mikrot.generate_pass()
    if myrouter.change_wifi_passwd(new_password):
        msg=success_message.format(new_password)
    else: msg=error_message
    recipients = [client.strip() for client in mail_clients.split(',')]
    logging.info(f'Sending email with a new password:{myrouter.get_pass} to {recipients}')
    #send_mail('test@mhch.ru',recipients,msg,subject='Monthly WIFI password change')
    logging.info(f'The script successfully finished, the mail sent, new password: {myrouter.get_pass} the old one: {myrouter.get_expass}')
    print(msg)
    print(f'The previouse password was {myrouter.get_expass()}')
if __name__=="__main__":
    main_prog()
    
