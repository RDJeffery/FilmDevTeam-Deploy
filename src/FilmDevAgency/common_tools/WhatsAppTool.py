from agency_swarm.tools import BaseTool
from pydantic import Field
from twilio.rest import Client
import os
from typing import ClassVar
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WhatsAppTool(BaseTool):
    """
    WhatsApp Communication Tool to send messages via WhatsApp using Twilio's API.
    
    Required Environment Variables (.env file):
    - TWILIO_ACCOUNT_SID: Your Twilio Account SID
    - TWILIO_AUTH_TOKEN: Your Twilio Auth Token
    - TWILIO_WHATSAPP_NUMBER: Your Twilio WhatsApp number (without 'whatsapp:' prefix)
    """
    name: ClassVar[str] = "WhatsApp Communication Tool"
    description: ClassVar[str] = "Sends messages via WhatsApp using Twilio"

    # Fields to define inputs for the tool dynamically
    to_number: str = Field(
        ..., description="Recipient's WhatsApp number (with or without 'whatsapp:' prefix)"
    )
    message: str = Field(
        ..., description="The message content to be sent via WhatsApp."
    )

    def run(self) -> str:
        """
        Executes the WhatsApp message sending process.
        
        Returns:
            str: A confirmation message if successful, or an error message if failed.
        """
        # Retrieve Twilio credentials from environment variables
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        
        if not account_sid or not auth_token or not from_number:
            return """Error: Twilio environment variables are not properly set. 
            Please ensure you have created a .env file with:
            TWILIO_ACCOUNT_SID=your_account_sid
            TWILIO_AUTH_TOKEN=your_auth_token
            TWILIO_WHATSAPP_NUMBER=your_whatsapp_number"""

        client = Client(account_sid, auth_token)

        # Send the message
        try:
            sent_message = client.messages.create(
                from_=f'whatsapp:{from_number}',
                body=self.message,
                to=f'whatsapp:{self.to_number}' if not self.to_number.startswith('whatsapp:') else self.to_number
            )
            return f"Message sent successfully! SID: {sent_message.sid}"
        except Exception as e:
            return f"Failed to send message: {str(e)}"


if __name__ == "__main__":
    # Example usage
    tool = WhatsAppTool(
        to_number="+27718875225",  # The number will be automatically formatted with whatsapp: prefix
        message="Hello, this is a test message from WhatsApp Tool!"
    )
    print(tool.run()) 