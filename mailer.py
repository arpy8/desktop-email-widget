import json
import email
import imaplib
import logging
from email.header import decode_header

from llm import enhance_email_data
from config import USER_EMAIL, USER_PASSWORD

logger = logging.getLogger(__name__)


def determine_priority(subject, body):
    high_keywords = ['urgent', 'deadline', 'asap', 'important', 'critical', 'emergency', 'selection', 'offer', 'interview', 'last']
    medium_keywords = ['meeting', 'reminder', 'update', 'registration', 'application', 'hackathon']
    
    content = (subject + ' ' + body).lower()
    
    for keyword in high_keywords:
        if keyword in content:
            return 'high'
    
    for keyword in medium_keywords:
        if keyword in content:
            return 'medium'
    
    return 'low'

def get_mail_data(data):
    logger.debug("Processing email data")
    try:
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                        break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")

        email_data = {
            "date": msg.get("Date"),
            "subject": subject.replace('\n', ' ').replace('\r', ' ')[:100],
            "from": msg.get("From"),
            "to": msg.get("To"),
            "body": body.replace('\n', ' ').replace('\r', ' ')[:1000],
            "priority": determine_priority(subject, body)
        }
        
        logger.debug(f"Processed email: {email_data['subject'][:50]}...")
        return email_data
        
    except Exception as e:
        logger.error(f"Error processing email data: {str(e)}")
        raise
    
def get_last_n_mails(n=1, no_enhance=False):
    logger.info(f"Fetching last {n} emails from Gmail")
    try:
        M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        M.login(USER_EMAIL, USER_PASSWORD)
        M.select()

        _, message_numbers = M.search(None, 'ALL')

        rslt = []
        for num in message_numbers[0].split()[-n:][::-1]:
            _, data = M.fetch(num, '(RFC822)')
            email_data = get_mail_data(data)
            rslt.append(email_data)

            del data

        M.close()
        M.logout()
        
        logger.info(f"Successfully fetched {len(rslt)} emails")
        
        if no_enhance:
            return json.dumps(
                rslt, 
                indent=4, 
                ensure_ascii=False
            )

        return enhance_email_data(
                                    json.dumps(
                                                rslt, 
                                                indent=4, 
                                                ensure_ascii=False
                                            )
                                )
    except Exception as e:
        logger.error(f"Error fetching emails: {str(e)}")
        raise

if __name__ == "__main__":
    print(get_last_n_mails(10))