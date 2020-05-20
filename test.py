"""
Initial script for testing. Ignore this file.
"""

import urllib
from bs4 import BeautifulSoup
from urllib import request
from urllib.error import URLError
import time
import shelve
from threading import Thread
headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

#res=requests.get('https://cricbuzz.com/live-cricket-scores/22458/',allow_redirects=False) #cricbuzz is rejecting anonymous requests without headers and redirecting it to home page
#src=res.content
#htmlElem=html.document_fromstring(src)
#temp=htmlElem.cssselect("[class=cb-ovr-flo]")
#for i in temp:
    #print(i.text_content())

#print(src)
#print("end")

def sendemail():
    # import smtplib,ssl
    #
    # port=465
    # smtp_server='smtp.gmail.com'
    # msg='''Yay! it's a six!'''

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import shelve

    sender_email = 'gvp.webchamp@gmail.com'
    #receiver_email = 'rohitbabug81@gmail.com'
    password = 'webchamp@2k19'

    message = MIMEMultipart("alternative")
    message["Subject"] = "It's a SIX! in the match"
    message["From"] = sender_email
    #message["To"] = receiver_email
    # message['Bcc']=receiver_email
    # Create the plain-text and HTML version of your message
    html = """\
    <html>
      <body>
        <center><h2><b>Yay!</b><br>
           That's a <b style="color:red">Six!</b><br>
        </h2>
        <h3>Apply <span style="color:red">SWIGGY6</span> within 6 mins and enjoy 60% OFF upto 75</h3>
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
        m_idobj.clear()
        m_id = m_idobj['m_id']
        #m_id=list(m_id)
        print(m_id)
        m_idobj['m_id']=str(int(m_id)+1)
    except (KeyError,TypeError):
        m_idobj['m_id']='22483'
        m_id=str(int(m_idobj['m_id'])-1)


def bs():
    old_ball_no = '0.0'
    while True:
        try:
            url = 'https://www.cricbuzz.com/live-cricket-scores/' + m_id + '/'
            # url = 'https://www.cricbuzz.com/live-cricket-scores/22462/'
            req = urllib.request.Request(url=url, headers=headers)
            html = urllib.request.urlopen(req)
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup.prettify())

            # class ="cb-col cb-col-67 cb-nws-lft-col cb-comm-pg"
            root = soup.find('div', {'class': 'cb-col cb-col-100 cb-font-12 cb-text-gray cb-min-rcnt'})
            temp = soup.find('div', {'class': "cb-mat-mnu-wrp cb-ovr-num"})
            # check point before match start
            curr_ball_no = str(list(temp)[0])
            if '.6' in curr_ball_no:
                # print('_____________Over complete_______')
                print("temp", curr_ball_no)
                yield 'over complete'
                # time.sleep(18)
            if '19.6' in curr_ball_no:
                old_ball_no = '0.0'
                yield 'innings complete'
            # print('test: ',root)
            #print(type(curr_ball_no),type(old_ball_no))
            #print((curr_ball_no), (old_ball_no))
            if float(curr_ball_no) <= float(old_ball_no):
                print('same ball')
                time.sleep(2)
                continue
                # time.sleep(2)
            else:
                try:
                    # print("1:", list(root.span.next_sibling))
                    print("temp", curr_ball_no)
                    data = list(root.span.next_sibling)[0].strip().replace("|", "").split(" ")
                    # print(len(data))
                    # print(data)
                    # print(data[len(data) - 2], data[len(data) - 1])
                    # print("Match complete!")
                    # main=soup.find('div',{'ng-show':'!isCommentaryRendered'})
                    # comm=main.find('div',{'class':'"cb-col cb-col-100"'})
                    # comm=main.div
                    # l=list(comm)
                    # print(main)
                    # print('--------------------------------')
                    # print(comm)
                    # print(l)
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
    try:
        res = next(gen)
        if res == 'complete':
            break
        elif res == True:
            print("Six!")
            Thread(target=sendemail).start()
            time.sleep(15)  # 45
        elif res == 'over complete':  # what if last ball is six? need to add condition #done
            time.sleep(18)  # 70
        elif res == 'innings complete':
            time.sleep(900)
        else:
            time.sleep(15)  # 45
    except (TypeError,StopIteration):
        print('pass')
        time.sleep(10)
        pass
# start=time.time()
# while True:
#     bs()
