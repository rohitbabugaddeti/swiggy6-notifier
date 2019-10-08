# import smtplib,ssl
#
# port=465
# smtp_server='smtp.gmail.com'
# msg='''Yay! it's a six!'''


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shelve

sender_email='youremail'
#receiver_email = 'rohitbabug81@gmail.com'
password = 'yourpassword'

message = MIMEMultipart("alternative")
message["Subject"] = "It's a SIX! in the match"
message["From"] = sender_email
#message["To"] = receiver_email
#message['Bcc']=receiver_email
# Create the plain-text and HTML version of your message
text = """\
"""
html = """\
<html>
  <body>
    <center><h2><b>Yay!</b><br>
       That's a <b style="color:red">Six!</b><br>
    </h2>
    <h3>Apply <span style="color:red">SWIGGY6</span> within 6 mins and enjoy 60% OFF upto 75</h3>
    </center>
  </body>
</html>
"""


content = MIMEText(html, "html")



message.attach(content)

# Create secure connection with server and send email
context = ssl.create_default_context()
with shelve.open('test.db') as sobj:
    receiver_emails=sobj['emails']
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    for rec_mail_id in receiver_emails:
        server.sendmail(
            sender_email, rec_mail_id, message.as_string()
        )
