# Testing the Creative Director WhatsApp Functionality

This guide will help you test the Creative Director's WhatsApp communication functionality.

## Prerequisites

1. Make sure you have all required environment variables set in your `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
```

2. Ensure your Twilio WhatsApp Sandbox is set up:
   - Visit the [Twilio Console](https://console.twilio.com/)
   - Navigate to Messaging > Try it out > Send a WhatsApp Message
   - Follow the instructions to join your sandbox

## Running the Interactive Test

1. Activate your virtual environment:
```bash
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Run the test script:
```bash
python test_creative_director.py
```

3. Interact with the Creative Director:
   - The script starts with an initial project proposal
   - You can then type your responses/questions
   - Type 'exit' to end the session

## Expected Behavior

The Creative Director should:
1. Receive your messages in real-time
2. Respond with concise WhatsApp-style messages
3. Include appropriate emojis and status updates
4. Break down the development process into clear steps
5. Maintain context throughout the conversation

## Example Interactions

You can try messages like:
- "What's the current status of the project?"
- "Can we focus more on the visual aspects?"
- "What do you think about adding a conflict element?"
- "Could you share the latest script outline?"

## Troubleshooting

If you encounter issues:
1. Verify all environment variables are correctly set
2. Ensure your Twilio number is properly configured for WhatsApp
3. Check that your sandbox invitation was accepted
4. Review Twilio console for any error messages 