import imapclient
import smtplib
from email.message import EmailMessage
import pyzmail

def read_unread_emails(username, password):
    """Checks for and reads unread emails."""
    try:
        imap_server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        imap_server.login(username, password)
        imap_server.select_folder('INBOX')
        
        unread_ids = imap_server.search('UNSEEN')
        if not unread_ids:
            return "You have no unread emails."
        
        raw_message = imap_server.fetch(unread_ids, ['BODY[]'])
        message = pyzmail.PyzMessage.factory(raw_message[unread_ids[0]][b'BODY[]'])
        
        sender = message.get_addresses('from')[0]
        subject = message.get_subject()
        
        speak_text = f"You have {len(unread_ids)} new messages. The most recent is from {sender[0]} with the subject {subject}. Would you like me to read it?"
        
        imap_server.logout()
        return speak_text

    except Exception as e:
        return f"Sorry, I couldn't read your emails. Error: {e}"

def read_most_recent_email(username, password):
    """Reads the body of the most recent unread email."""
    try:
        imap_server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        imap_server.login(username, password)
        imap_server.select_folder('INBOX')

        all_ids = imap_server.search('UNSEEN')
        if not all_ids:
            return "You have no unread messages to read."

        raw_message = imap_server.fetch(all_ids[-1:], ['BODY[]'])
        message = pyzmail.PyzMessage.factory(raw_message[all_ids[-1]][b'BODY[]'])

        body = ""
        if message.text_part:
            body = message.text_part.get_payload().decode(message.text_part.charset)
        else:
            body = "This email contains no readable text."

        imap_server.logout()
        return body

    except Exception as e:
        return f"Sorry, I couldn't read the email. Error: {e}"
        
def send_email(username, password, recipient, subject, body):
    """Sends an email to a specified recipient."""
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = username
        msg['To'] = recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(username, password)
            smtp.send_message(msg)
        return "Your email has been sent successfully."
    except Exception as e:
        print(f"Email sending error: {e}")
        return "Sorry, I could not send the email."

def read_sent_emails(username, password):
    """Checks for and reads recent sent emails."""
    try:
        imap_server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        imap_server.login(username, password)
        # Note: The folder name may be 'Sent' or 'Sent Items' depending on your email provider.
        imap_server.select_folder('Sent', readonly=True)

        sent_ids = imap_server.search('ALL')
        if not sent_ids:
            return "Your sent folder is empty."
        
        # Read the 3 most recent sent emails
        recent_ids = sent_ids[-3:]
        
        response = "Here are your three most recent sent emails:"
        for msg_id in recent_ids:
            raw_message = imap_server.fetch(msg_id, ['BODY[]', 'RFC822', 'ENVELOPE'])
            message = pyzmail.PyzMessage.factory(raw_message[msg_id][b'BODY[]'])
            
            subject = message.get_subject()
            recipient = message.get_addresses('to')[0][1]
            
            response += f"\nTo: {recipient}\nSubject: {subject}\n---"
            
        imap_server.logout()
        return response
    except Exception as e:
        print(f"Sent email reading error: {e}")
        return "I'm sorry, I couldn't read your sent emails."