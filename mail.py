import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import flask
from flask_httpauth import HTTPBasicAuth
import requests
import time

import hashlib


#The mail addresses and password
sender_address = 'sender@gmail.com'
sender_pass = ''#the device auth password, availble below the 2nd auth in gmail
receiver_address = 'receiver@gmail.com'



app = flask.Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "root": "password@",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required  
def helloworld():
    return "Welcome\n"


@app.route('/Mail',methods=['POST'])
@auth.login_required  
def Mail():
    if flask.request.method == 'POST':
        data = flask.request.get_data()
        mail_content = data.decode()
        #data format: DEVICE_NAME;message
        if mail_content == "NOTHING":
            return "NOTHING\n"
        device = mail_content.split(';')[0]
        mail_content = mail_content.split(';')[1]
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'WANRING: LOGIN ON '+ device  #The subject line
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        #print(data)
    return 'Success\n'



@auth.error_handler
def unauthorized():
    return 'Could not verify your access level for that URL.  You have to login with proper credentials\n'
    
if __name__ == '__main__':
    app.run(host='yourip',port = 80,debug= False)


#Setup the MIME


#The body and the attachments for the mail


