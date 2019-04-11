import imaplib
import email
import shelve
emails=set()

#new_uid_list=[]
mail=imaplib.IMAP4_SSL("imap.gmail.com")
mail.login("gvp.webchamp@gmail.com","webchamp@2k19")
mail.list()
mail.select("inbox")

assam,data=mail.uid('search',None,'ALL')
uids_list=data[0].split()
#first_email_uid=uids_list[0]
#latest_email_uid=uids_list[-1]
#print(first_email_uid,latest_email_uid)
for i in uids_list[::-1]:
    assam,data=mail.uid('fetch',i,'(RFC822)')
    #skipping 0 index of data[0] as it contains uid info
    raw_email=data[0][1]
    raw_email_string=raw_email.decode('utf-8')
    email_message=email.message_from_string(raw_email_string)
    #print(data[0])
    email_from=str(email.header.make_header(email.header.decode_header(email_message['From'])))
    #email_subj=str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
    emails.add(email_from[email_from.index('<')+1:email_from.index('>')])
    print(email_from[email_from.index('<')+1:email_from.index('>')])
    #new_uid_list.append(i)
    mail.uid('STORE',i,'+X-GM-LABELS','\\Trash')

s=shelve.open('test.db',writeback=True)
#s.clear()
try:
    old=s['emails']
    print('old: ',s['emails'])
    old=old.union(emails)
    s['emails']=old
    print('updated old: ',s['emails'])
except KeyError:
    s['emails']=emails
    print(s['emails'])
finally:
    s.close()

# for i in new_uid_list:
#     print(i)

    # for resp_part in data:
    #     #raw_email = data[1]
    #     import email
    #     #email_message = email.message_from_string(resp_part)
    #     #print(resp_part)