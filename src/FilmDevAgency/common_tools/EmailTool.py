from agency_swarm.tools import BaseTool
from pydantic import Field
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for SMTP server
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


class ScriptNotepadEmailTool(BaseTool):
    """
    A tool to facilitate saving chat segments and emailing reformatted scripts.
    It allows the creative director to compose and send an email with the content.
    """
    recipient_email: str = Field(..., description="The email address of the recipient.")
    subject: str = Field(..., description="The subject line of the email.")
    chat_content: str = Field(..., description="Chat content or reformatted text to be included in the email.")

    def run(self) -> str:
        """
        Sends an email with the specified subject and content to the recipient.
        """
        # Debug information
        print("\nDebug Information:")
        print(f"Using email address: {EMAIL_ADDRESS}")
        print(f"App Password length: {len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 0} characters")
        print(f"Sending to: {self.recipient_email}")
        
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            return "Error: Email credentials are missing. Please check your .env file."

        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = EMAIL_ADDRESS
            message["To"] = self.recipient_email
            message["Subject"] = self.subject
            message.attach(MIMEText(self.chat_content, "plain"))

            # Connect to server
            print("\nConnecting to Gmail SMTP server...")
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.set_debuglevel(1)  # Enable debug output
            
            # Start TLS
            print("Enabling TLS...")
            server.starttls()
            
            # Login
            print("Attempting login...")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            # Send email
            print("Sending email...")
            server.send_message(message)
            
            # Cleanup
            print("Closing connection...")
            server.quit()
            
            return "Email sent successfully!"
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"""
Authentication Error: {str(e)}

Troubleshooting Steps:
1. Verify 2-Step Verification is enabled in your Google Account
2. Generate a new App Password:
   - Go to Google Account Settings
   - Security
   - 2-Step Verification
   - App Passwords
   - Select 'Mail' and 'Other (Custom name)'
3. Copy the new 16-character password (no spaces)
4. Update GMAIL_APP_PASSWORD in your .env file

Current Settings:
- Email: {EMAIL_ADDRESS}
- Password Length: {len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 0} characters (should be 16)
"""
            return error_msg
            
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    # Test case
    test_tool = ScriptNotepadEmailTool(
        recipient_email="rickdodge@hotmail.co.za",
        subject="Test Email",
        chat_content="This is a test email to verify the email functionality."
    )
    print(test_tool.run())