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
    email_subj=str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
    print('email subject: ',email_subj)
    if 'remove' in email_subj.replace(' ','').lower():
        s=shelve.open('test.db',writeback=True)
        mails=s['emails']
        print('before removal: ',mails)
        e_id=email_from[email_from.index('<') + 1:email_from.index('>')]
        try:
            mails.remove(e_id)
            s['emails'] = mails
        except KeyError:
            pass
        #condition to check if remove requestd mail is already present in current read and removing it from current read emails set
        if e_id in emails:
            print('emails before remove',emails)
            print('removed ',e_id ,' from current read')
            emails.remove(e_id)
        print('remove sucess')
        print('after removal: ',s['emails'])
        s.close()
        mail.uid('STORE', i, '+X-GM-LABELS', '\\Trash')
    else:
        try:
            emails.add(email_from[email_from.index('<') + 1:email_from.index('>')])
            #print(email_from[email_from.index('<') + 1:email_from.index('>')])
            #print(emails)
            # new_uid_list.append(i)
            mail.uid('STORE', i, '+X-GM-LABELS', '\\Trash')
        except ValueError:
            pass
print('-----------------------------')
print(emails)
print('------------------------------')
s=shelve.open('test.db',writeback=True)
#s.clear()
try:
    old=s['emails']
    print('old: ',s['emails'])
    old.update(emails)
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
