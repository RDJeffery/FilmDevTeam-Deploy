import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

# Verify environment variables
def check_environment():
    required_vars = [
        'OPENAI_API_KEY',
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_WHATSAPP_NUMBER'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease add these to your .env file")
        return False
    return True

def main():
    # Check environment variables first
    if not check_environment():
        return

    try:
        from FilmDevAgency.CreativeDirector import CreativeDirector
        from agency_swarm import Agency
        
        # Initialize the Creative Director
        creative_director = CreativeDirector()
        
        # Create the agency with just the Creative Director for testing
        agency = Agency([creative_director])
        
        print("🎬 Creative Director WhatsApp Test Session")
        print("Type 'exit' to end the session\n")
        
        # Initial test message
        test_message = """
        Hi Creative Director, I have a new project idea. 
        I'd like to develop a short film about a person who discovers they can communicate with plants. 
        Could you help coordinate the development of this idea?
        """
        
        # Send the initial message
        print("\nYOU: " + test_message.strip())
        response = agency.get_completion(test_message)
        print("\nCREATIVE DIRECTOR: " + response)
        
        # Interactive loop for continued conversation
        while True:
            # Get user input
            user_message = input("\nYOU (type 'exit' to end): ").strip()
            
            # Check for exit command
            if user_message.lower() == 'exit':
                print("\n👋 Ending test session...")
                break
            
            # Send message to Creative Director
            if user_message:
                response = agency.get_completion(user_message)
                print("\nCREATIVE DIRECTOR: " + response)
                
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease check your environment variables and API keys.")

if __name__ == "__main__":
    main() 