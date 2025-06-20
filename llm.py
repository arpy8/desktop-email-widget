import json
import logging
import google.generativeai as genai

from utils import janitor_bhaiyo
from config import LLM_INSTRUCTIONS, GEMINI_API_KEY

logger = logging.getLogger(__name__)


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def enhance_email_data(email_data):
    logger.info("Starting email enhancement process")
    emails = json.loads(email_data)
    enhanced_emails = []
    
    for i, email in enumerate(emails):
        logger.debug(f"Processing email {i+1}/{len(emails)}: {email.get('subject', 'No Subject')[:50]}")
        
        essential_email = {
            'subject': email.get('subject', ''),  
            'body': email.get('body', '')[:1000],        
            'from': email.get('from', ''),
            'date': email.get('date', ''),
            'priority': email.get('priority', 'medium')
        }
        
        prompt = LLM_INSTRUCTIONS.format(
            email_subject=essential_email['subject'],
            email_body=essential_email['body'],
            email_from=essential_email['from'],
            email_date=essential_email['date']
        )
        
        try:
            logger.debug(f"Sending email to LLM for enhancement: {essential_email['subject'][:30]}")
            response = model.generate_content(prompt)
            ai_response = json.loads(janitor_bhaiyo(response.text))
            essential_email['body'] = ai_response.get('summary', essential_email['body'][:200])
            essential_email['priority'] = ai_response.get('priority', 'medium')
            essential_email['date'] = ai_response.get('date', essential_email['date'])
            logger.debug(f"Successfully enhanced email: {essential_email['subject'][:30]}")
        except Exception as e:
            logger.error(f"LLM processing error for email '{essential_email['subject'][:30]}': {e}")
            essential_email['body'] = essential_email['body'][:200]
        
        enhanced_emails.append(essential_email)
        
        del prompt
        if 'response' in locals():
            del response
        if 'ai_response' in locals():
            del ai_response
    
    logger.info(f"Enhanced {len(enhanced_emails)} emails successfully")
    return json.dumps(
                        enhanced_emails, 
                        indent=4, 
                        ensure_ascii=False
                    )


# if __name__ == "__main__":
#     import logging
#     logging.basicConfig(level=logging.INFO)
#     logger = logging.getLogger(__name__)
    
#     logs_file = "logs.json"
    
#     if not os.path.exists(logs_file):
#         logger.info("logs.json not found. Fetching and enhancing emails...")
        
#         email_data = get_last_n_mails(10)
#         logger.info("Fetched email data:")
#         print(email_data)
        
#         enhanced_data = enhance_email_data(email_data)
#         logger.info("Enhanced email data:")
#         print(json.loads(enhanced_data))
        
#         with open(logs_file, "w", encoding="utf-8") as f:
#             f.write(enhanced_data)
        
#         logger.info(f"Enhanced emails saved to {logs_file}")
#     else:
#         logger.info(f"{logs_file} already exists. Skipping email fetch and enhancement.")