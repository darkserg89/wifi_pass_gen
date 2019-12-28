# -*- coding: utf-8 -*-
import netmiko
import string
import random
from mailer import send_mail
import os
import re


ip = os.environ.get('mik_ip')
login = os.environ.get('mik_login')
password = os.environ.get('mik_pass')
port=os.environ.get('mik_port')
command='/interface wireless security-profiles print detail value-list'
mydev = {'device_type':"mikrotik_routeros","username":login,'password':password,'ip':ip}

mail_message = '''
Hello, The Password of the Guest WIFI has been changed.
SSID: MBMFWF
Password: {}
'''


class Mikrot:
    def __init__(self,login,password,ip,port=22):
        self.username=login
        self.password=password
        self.ip=ip
        self.port=port
        self.dev={'device_type':"mikrotik_routeros","username":self.username,"password":self.password,'ip':self.ip,'port':self.port}
        
    def _generate_pass(length=8):
        'Generate password with the length'
        symbols=string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choices(symbols,k=length))
    
    def show_command(self,command):
        with netmiko.ConnectHandler(**self.dev,default_enter="\n\r") as ssh:
            result=ssh.send_command(command)
        return result

    def change_wifi_passwd(self,new_password):
        re_pat='wpa2-pre-shared-key=\"(\w+)\"'
        cmd_get_current_pass='/interface wireless security-profile print'
        cmd_passwd_change='/interface wireless security-profiles set comment={new_pass}'
        raw_current_pass = self.show_command(cmd_get_current_pass)
        
        
        try:
            with netmiko.ConnectHandler(**self.dev,default_enter="\n\r") as ssh:
                ssh.send_command(cmd_passwd_change.format(new_password))
        except:
            return False
        self._prev_pass=re.search(re_pat,raw_current_pass).group(1) #still not set
        self._current_pass=new_password
        return True
    
    @property
    def get_pass(self):
        return self._current_pass
    @property
    def get_priv_pass(self):
        return self._prev_pass

	
if __name__=="__main__":
    myrouter=Mikrot(login=login,password=password,ip=ip)
    print(myrouter.show_command(command))
    myrouter.change_wifi_passwd('test_passwd')
    print(myrouter.get_pass)
    print(myrouter.get_priv_pass)
    
