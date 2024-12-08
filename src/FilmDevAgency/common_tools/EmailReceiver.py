import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
import email.utils

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class EmailReceiver:
    def __init__(self):
        self.email_address = os.getenv("GMAIL_ADDRESS")
        self.password = os.getenv("GMAIL_APP_PASSWORD")
        self.imap_server = "imap.gmail.com"
        self.allowed_sender = os.getenv("ALLOWED_SENDER_EMAIL")
        logger.info(f"EmailReceiver initialized with email: {self.email_address}, allowed sender: {self.allowed_sender}")
        
    def connect(self):
        """Establish connection to Gmail IMAP server"""
        logger.info("Connecting to Gmail IMAP server...")
        self.imap = imaplib.IMAP4_SSL(self.imap_server)
        self.imap.login(self.email_address, self.password)
        logger.info("Successfully connected to Gmail IMAP server")
        
    def is_recent_email(self, message):
        """Check if email was received in the last 60 seconds"""
        date_str = message.get('Date')
        if not date_str:
            return False
            
        # Parse the email date
        try:
            parsed_date = email.utils.parsedate_to_datetime(date_str)
            if parsed_date.tzinfo is None:  # Make naive datetime timezone-aware
                parsed_date = parsed_date.replace(tzinfo=datetime.now().astimezone().tzinfo)
                
            # Get current time
            current_time = datetime.now(parsed_date.tzinfo)
            
            # Check if email is within last 60 seconds
            time_difference = current_time - parsed_date
            is_recent = time_difference <= timedelta(seconds=60)
            
            if is_recent:
                logger.info(f"Email is recent (received {time_difference.total_seconds():.1f} seconds ago)")
            else:
                logger.info(f"Email is not recent (received {time_difference.total_seconds():.1f} seconds ago)")
                
            return is_recent
            
        except Exception as e:
            logger.error(f"Error parsing email date: {str(e)}")
            return False
        
    def get_latest_emails(self, num_emails=5, filter_sender=True):
        """Fetch the latest emails from inbox"""
        try:
            self.connect()
            self.imap.select("INBOX")
            logger.info(f"Checking for latest {num_emails} emails...")
            
            # Search for all emails in inbox
            _, message_numbers = self.imap.search(None, "ALL")
            
            email_list = []
            # Get all email IDs
            email_ids = message_numbers[0].split()
            email_ids.reverse()  # Most recent first
            
            processed_count = 0
            logger.info(f"Found {len(email_ids)} total emails")
            
            for email_id in email_ids:
                if processed_count >= num_emails:
                    break
                    
                logger.info(f"Processing email ID: {email_id}")
                _, msg_data = self.imap.fetch(email_id, "(RFC822)")
                email_body = msg_data[0][1]
                message = email.message_from_bytes(email_body)
                
                # Check if email is recent
                if not self.is_recent_email(message):
                    logger.info("Skipping old email")
                    continue
                
                sender = decode_header(message["from"])[0][0]
                if isinstance(sender, bytes):
                    try:
                        sender = sender.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            sender = sender.decode('latin-1')
                        except UnicodeDecodeError:
                            sender = sender.decode('utf-8', errors='ignore')
                
                logger.info(f"Email from: {sender}")
                
                # Skip if filtering by sender and it's not the allowed sender
                if filter_sender and self.allowed_sender and self.allowed_sender.lower() not in sender.lower():
                    logger.info(f"Skipping email from {sender} - not from allowed sender")
                    continue
                
                subject = decode_header(message["subject"])[0][0]
                if isinstance(subject, bytes):
                    try:
                        subject = subject.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            subject = subject.decode('latin-1')
                        except UnicodeDecodeError:
                            subject = subject.decode('utf-8', errors='ignore')
                
                logger.info(f"Processing email with subject: {subject}")
                
                # Get email content
                content = ""
                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == "text/plain":
                            payload = part.get_payload(decode=True)
                            if payload:
                                try:
                                    content = payload.decode('utf-8')
                                except UnicodeDecodeError:
                                    try:
                                        content = payload.decode('latin-1')
                                    except UnicodeDecodeError:
                                        content = payload.decode('utf-8', errors='ignore')
                            break
                else:
                    payload = message.get_payload(decode=True)
                    if payload:
                        try:
                            content = payload.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                content = payload.decode('latin-1')
                            except UnicodeDecodeError:
                                content = payload.decode('utf-8', errors='ignore')
                
                email_list.append({
                    "id": email_id,
                    "subject": subject,
                    "sender": sender,
                    "content": content,
                    "date": message.get('Date')
                })
                processed_count += 1
                logger.info(f"Successfully processed email: {subject}")
            
            logger.info(f"Processed {len(email_list)} emails matching criteria")
            return email_list
            
        except Exception as e:
            logger.error(f"Error processing emails: {str(e)}")
            raise
        finally:
            logger.info("Closing IMAP connection")
            self.imap.close()
            self.imap.logout()
            
    def check_new_emails(self):
        """Check for new emails from the allowed sender"""
        if not self.allowed_sender:
            logger.warning("No allowed sender configured")
            return None
        logger.info("Checking for new emails from allowed sender")
        try:
            emails = self.get_latest_emails(num_emails=1, filter_sender=True)
            if emails:
                logger.info("Found new email from allowed sender")
                return emails[0]
            logger.info("No new emails from allowed sender")
            return None
        except Exception as e:
            logger.error(f"Error checking new emails: {str(e)}")
            return None 