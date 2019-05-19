import imaplib
import email

mail=imaplib.IMAP4_SSL("imap.gmail.com")
email_id=input("enter your email id:")
password=input("enter your password:")
try:
    mail.login(email_id,password)
except Exception as e:
    print(e)
mail.select('inbox')
a,data=mail.uid('search',None,'ALL')
uids_list=data[0].split()
for i in uids_list[::-1]:
    assam, data = mail.uid('fetch', i, '(RFC822)')
    # skipping 0 index of data[0] as it contains uid info
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    # print(data[0])
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    if email_from[email_from.index('<') + 1:email_from.index('>')]==input('enter the spam mail id'):
        mail.uid('STORE', i, '+X-GM-LABELS', '\\Trash')
        print('deleted mail with uid ',i)