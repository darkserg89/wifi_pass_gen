# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def msg_generator(msg_list):
    result = '\n'.join(msg_list)
    return result            


def send_mail(from_addr, to_addr, message_text, subject='No Subject',bcc = [],smtp_server_ip='203.59.72.37',smtp_port = '25', smtp_auth = False, smtp_login = None, smtp_pass = None, tls=False):
    '''The function is sending email notification '''
    msg = MIMEMultipart()
    msg['From']=from_addr
    msg['To']=to_addr
    msg['Subject'] = subject
    body =  message_text
    #Creating a msg based on PLAIN text
    msg.attach(MIMEText(body,'plain'))
    #Convert msg to string
    text_msg = msg.as_string()


    #Sending a mail to server
    smtp_server =  smtplib.SMTP(smtp_server_ip,smtp_port)
    #Testing the connection
    smtp_server.ehlo()
    if smtp_auth:
        smtp_server.login(smtp_login,smtp_pass)
        if tls:
            smtp.starttls()
    smtp_server.sendmail(from_addr,[to_addr] + bcc, text_msg)
    smtp_server.quit()