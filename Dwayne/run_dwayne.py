import mailbox
import uuid
import email.utils
import sqlite3

import config
# config.py file

from email_reply_parser import EmailReplyParser
# https://github.com/zapier/email-reply-parser




# Load config variables from config.py
mbox = mailbox.mbox(config.DWAYNE_CONFIG['mailbox'])
NQUESTIONS = config.DWAYNE_CONFIG['NQUESTIONS']
db_name = config.DWAYNE_CONFIG['db_name']
question_1 = config.DWAYNE_CONFIG['question_1']
question_2 = config.DWAYNE_CONFIG['question_2']
question_3 = config.DWAYNE_CONFIG['question_3']
len1 = len(question_1)
len2 = len(question_2)
len3 = len(question_3)
uidstring = config.DWAYNE_CONFIG['uidstring']
lenid = len(uidstring)

def get_shortid(subject_line):
    """
    Returns the short id from the email subject
    """
    shortid = None
    # TODO check parsing method
    if uidstring in subject_line:
        shortid = subject_line[ subject_line.find(uidstring) + lenid : ]
    return shortid

def get_body(message):
    """
    Returns the body of a message. 
    Escapes pitfalls about multipart, attachments etc.
    """
    body = ""
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)
                break
    else:
        body = message.get_payload(decode=True)
    body = body.decode('UTF-8')
    return body
    
def parse_body(whole_body):
    """
    Uses `email_reply_parser` to only fetch the latest message.
    Also strips trailing and leading characters.
    Returns a list of the text between the `Questions` provided. 
    """
    # TODO Automate and prettify the function
    # Can it be implemented without email_reply_parser?
    answers = []
    body  = EmailReplyParser.parse_reply(whole_body) # Latest reply only
    body = body.replace('\n', ' ').replace('\r', '').replace('  ' ,' ')

    answ1 = body[ body.find(question_1) + len1 : body.find(question_2) ].strip()
    answ2 = body[ body.find(question_2) + len2 : body.find(question_3) ].strip()
    answ3 = body[ body.find(question_3) + len3 :  ].strip()
    answers.extend([answ1, answ2, answ3])
    return answers

def generate_shortid():
    """
    Generates and returns a short id based on a random `uuid`.
    """
    return uuid.uuid4().hex[:7]

def get_info(message):
    """
    Returns a dictionary of information from the mbox headers.
    The list contains `From`, `To`, `Date`, and `Subject`
    """
    try:
        from_info = message.get('From', 'No sender provided')
        to_info = message.get('To', 'No recipient provided')
        date_info = message.get('Date', 'No date provided')
        subj_info = message.get('Subject', 'No subject provided')
    except:
        print('Didnt provide correct email object instance')
        raise
    return {'From':from_info, 'To':to_info ,'Date':date_info, 'Subject':subj_info }

def filter_messages(message):
    pass

def handle_timestamp(date):
    """
    Convert the mbox default `RFC 822` timestamp.
    Returns the ISO8601-compliant equivalent to be used with SQLite
    """
    assert isinstance(date, str), 'argument passed is not of type `string`'
    isodate = email.utils.parsedate_to_datetime(date)
    isodate = isodate.isoformat()
    return str(isodate)


conn = sqlite3.connect(db_name)
c = conn.cursor()



for msg in mbox:
    bd = get_body(msg)
    info = get_info(msg);
    subj = info['Subject']
    
    if uidstring in subj:
        #print('I found an email that should be a Standup')

        shortid= get_shortid(subj)
        isodate = handle_timestamp(info['Date'])
        mboxdate = info['Date']
        sender = info['From']
        recipient = info['To']
        all_answers = parse_body(bd)
        answ1 = all_answers[0]
        answ2 = all_answers[1]
        answ3 = all_answers[2]
        
        inserts = [shortid, isodate, mboxdate, sender, recipient, subj, answ1, answ2, answ3]

        c.execute(""" INSERT INTO standups
        (uid, 
        isodate, 
        mboxdate, 
        sender, 
        recipient, 
        subject,
        answ1, 
        answ2, 
        answ3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, inserts)

print("\nClosing connection to database. . .")
conn.commit()
conn.close()
