# import smtplib,ssl
#
# port=465
# smtp_server='smtp.gmail.com'
# msg='''Yay! it's a six!'''


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email='gvp.webchamp@gmail.com'
# receiver_email = 'rohitbabug81@gmail.com'
receiver_email = 'abcd@tbdn.com'
password = 'webchamp@2k19'

message = MIMEMultipart("alternative")
message["Subject"] = "It's a SIX! in the match"
message["From"] = sender_email
message["To"] = receiver_email
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

# Turn these into plain/html MIMEText objects
#part1 = MIMEText(text, "plain")
content = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
#message.attach(part1)
message.attach(content)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )