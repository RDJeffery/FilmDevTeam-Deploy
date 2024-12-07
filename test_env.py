from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Test all environment variables
def test_env_variables():
    variables = [
        'OPENAI_API_KEY',
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_WHATSAPP_NUMBER'
    ]
    
    print("Environment Variables Test:")
    print("-" * 30)
    
    all_present = True
    for var in variables:
        value = os.getenv(var)
        status = "✅ Present" if value else "❌ Missing"
        print(f"{var}: {status}")
        if not value:
            all_present = False
    
    print("-" * 30)
    if all_present:
        print("All required environment variables are present!")
    else:
        print("Some environment variables are missing!")
        
    # Print the actual path where dotenv is looking for the .env file
    print("\nDebug Information:")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Looking for .env file in: {os.path.abspath('.')}")

if __name__ == "__main__":
    test_env_variables() 