#using shelve, we store load id into a variable and override the value of id on disk (with 1 increment) only once in the whole run and
import urllib
from bs4 import BeautifulSoup
from urllib import request
from urllib.error import URLError
import time
import shelve
from threading import Thread
headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
def sendemail():
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import shelve

    sender_email = 'swiggy6notifier@gmail.com'
    password = 'rohit@swiggy6'

    message = MIMEMultipart("alternative")
    message["Subject"] = "It's a SIX! in the match"
    message["From"] = sender_email
    html = """\
        <html>
          <body>
            <center><h2><b>Yay!</b><br>
               That's a <b style="color:red">Six!</b><br>
            </h2>
            <h3>Apply <span style="color:red">SWIGGY6</span> within 6 mins and enjoy 60% OFF upto 60</h3>
            <a href='https://www.swiggy.com/'>click here</a>
            </center>
          </body>
        </html>
        """

    content = MIMEText(html, "html")

    message.attach(content)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with shelve.open('test.db') as sobj:
        receiver_emails = sobj['emails']
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        for rec_mail_id in receiver_emails:
            server.sendmail(
                sender_email, rec_mail_id, message.as_string()
            )

    print('email sending done!')

with shelve.open('m_id.db') as m_idobj:
    try:
        #m_idobj.clear()
        m_id = m_idobj['m_id']
        print(m_id)
        m_idobj['m_id']=str(int(m_id)+1)
    except (KeyError,TypeError):
        m_idobj['m_id']='22481'
        m_id=str(int(m_idobj['m_id'])-1)

def bs():
    old_ball_no = '0.0'
    while True:
        try:
            url = 'https://www.cricbuzz.com/live-cricket-scores/' + m_id + '/'
            req = urllib.request.Request(url=url, headers=headers)
            html = urllib.request.urlopen(req)
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup.prettify())
            root = soup.find('div', {'class': 'cb-col cb-col-100 cb-font-12 cb-text-gray cb-min-rcnt'})
            temp = soup.find('div', {'class': "cb-mat-mnu-wrp cb-ovr-num"})
            # check point before match start
            curr_ball_no = str(list(temp)[0])
            if '.6' in curr_ball_no:
                # print('_____________Over complete_______')
                print("temp", curr_ball_no)
                # if float(curr_ball_no) <= float(old_ball_no):
                #     print('same ball')
                #     time.sleep(1)
                #     continue
                #yield 'over complete'
                time.sleep(20)
            if float(curr_ball_no) <= float(old_ball_no):
                print('same ball')
                time.sleep(2)
                continue
            else:
                try:
                    print("temp", curr_ball_no)
                    data = list(root.span.next_sibling)[0].strip().replace("|", "").split(" ")
                    if '6' in data[len(data) - 1]:
                        if old_ball_no == curr_ball_no:
                            yield False
                        else:
                            yield True
                    else:
                        yield False
                    old_ball_no = list(temp)[0]
                except Exception as e:
                    # print("Match Complete!")
                    print(e)
                    yield 'complete'
        except (ConnectionResetError,URLError):
            pass
        except ValueError as ve:
            print(ve)

gen=bs()
while True:
    res=next(gen)
    if res=='complete':
        break
    elif res==True:
        print("Six!")
        Thread(target=sendemail).start()
        time.sleep(15) #45
    # elif res=='over complete':
    #     time.sleep(20) #70
    else:
        time.sleep(15) #45