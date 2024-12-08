from agency_swarm import Agency
import logging
import time
import os
from pathlib import Path
from dotenv import load_dotenv
import threading
from .common_tools.EmailReceiver import EmailReceiver
from .common_tools.EmailTool import ScriptNotepadEmailTool

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FilmDevAgency(Agency):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email_receiver = EmailReceiver()
        self.email_monitoring = False
        self.monitor_thread = None
        logger.info("FilmDevAgency initialized with email monitoring capability")

    def start_email_monitoring(self):
        """Start monitoring emails in a separate thread"""
        if not self.email_monitoring:
            logger.info("Starting email monitoring thread")
            self.email_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_emails)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            logger.info("Email monitoring thread started")
        else:
            logger.info("Email monitoring already running")

    def stop_email_monitoring(self):
        """Stop monitoring emails"""
        if self.email_monitoring:
            logger.info("Stopping email monitoring")
            self.email_monitoring = False
            if self.monitor_thread:
                self.monitor_thread.join()
            logger.info("Email monitoring stopped")
        else:
            logger.info("Email monitoring was not running")

    def _monitor_emails(self):
        """Monitor emails and route them to the Creative Director"""
        logger.info("Email monitoring loop started")
        while self.email_monitoring:
            try:
                logger.info("Checking for new emails...")
                new_email = self.email_receiver.check_new_emails()
                if new_email:
                    logger.info(f"Processing new email with subject: {new_email['subject']}")
                    
                    # Get the Creative Director agent
                    creative_director = next((agent for agent in self.agents if agent.name == "Creative Director"), None)
                    if not creative_director:
                        logger.error("Creative Director agent not found")
                        continue

                    # Create a new thread for this conversation
                    thread = creative_director.create_thread()
                    
                    # Process the email through the Creative Director
                    response = creative_director.run_thread(thread, new_email["content"])
                    logger.info("Generated response through Creative Director")
                    
                    # Send response back via email
                    logger.info(f"Sending response to: {new_email['sender']}")
                    email_tool = ScriptNotepadEmailTool(
                        recipient_email=new_email["sender"],
                        subject=f"Re: {new_email['subject']}",
                        chat_content=response
                    )
                    result = email_tool.run()
                    logger.info(f"Email response result: {result}")
                else:
                    logger.info("No new emails to process")
                
                # Wait for 60 seconds before checking again
                logger.info("Waiting 60 seconds before next check...")
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in email monitoring: {str(e)}")
                logger.error("Full error details:", exc_info=True)
                time.sleep(60)  # Wait before retrying

# Setup required directories
def setup_required_directories():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agents = [
        'CreativeDirector',
        'Researcher',
        'BrainstormingAgent',
        'IdeationAgent',
        'Scriptwriter1',
        'Scriptwriter2'
    ]
    subdirs = ['files', 'schemas', 'tools']
    
    for agent in agents:
        agent_dir = os.path.join(base_dir, agent)
        for subdir in subdirs:
            dir_path = os.path.join(agent_dir, subdir)
            os.makedirs(dir_path, exist_ok=True)
            logger.info(f"Created/verified directory: {dir_path}")

# Create directories before importing agents
logger.info("Setting up required directories...")
setup_required_directories()

# Debug imports
logger.info("Starting to import modules...")

try:
    from .CreativeDirector import CreativeDirector
    logger.info("CreativeDirector imported successfully")
    from .Researcher import Researcher
    logger.info("Researcher imported successfully")
    from .BrainstormingAgent import BrainstormingAgent
    logger.info("BrainstormingAgent imported successfully")
    from .IdeationAgent import IdeationAgent
    logger.info("IdeationAgent imported successfully")
    from .Scriptwriter1 import Scriptwriter1
    logger.info("Scriptwriter1 imported successfully")
    from .Scriptwriter2 import Scriptwriter2
    logger.info("Scriptwriter2 imported successfully")
except ImportError as e:
    logger.error(f"Import error occurred: {e}")
    raise

# Load environment variables from the FilmDevAgency/.env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Configure OpenAI API Key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

logger.info("Creating agent instances...")
creative_director = CreativeDirector('Creative Director')
researcher = Researcher('Researcher')
brainstorming_agent = BrainstormingAgent('Brainstorming Agent')
ideation_agent = IdeationAgent('Ideation Agent')
scriptwriter1 = Scriptwriter1('Scriptwriter 1')
scriptwriter2 = Scriptwriter2('Scriptwriter 2')
logger.info("All agent instances created successfully")

logger.info("Setting up agency...")
agency = FilmDevAgency([
       creative_director,  # Creative Director will be the entry point for communication with the user 
       [creative_director, researcher],  # Creative Director can initiate communication with Researcher
       [creative_director, brainstorming_agent],  # Creative Director can initiate communication with Brainstorming Agent
       [creative_director, ideation_agent],  # Creative Director can initiate communication with Ideation Agent
       [creative_director, scriptwriter1],  # Creative Director can initiate communication with Scriptwriter 1
       [creative_director, scriptwriter2],  # Creative Director can initiate communication with Scriptwriter 2
       [researcher, brainstorming_agent],  # Researcher can initiate communication with Brainstorming Agent
       [brainstorming_agent, ideation_agent],  # Brainstorming Agent can initiate communication with Ideation Agent
       [ideation_agent, scriptwriter1],  # Ideation Agent can initiate communication with Scriptwriter 1
       [ideation_agent, scriptwriter2],  # Ideation Agent can initiate communication with Scriptwriter 2
       [scriptwriter1, scriptwriter2],  # Scriptwriter 1 can initiate communication with Scriptwriter 2
       [scriptwriter2, researcher],  # Scriptwriter 2 can initiate communication with Researcher
       [scriptwriter1, researcher],  # Scriptwriter 1 can initiate communication with Researcher
       [scriptwriter1, creative_director],  # Scriptwriter 1 can initiate communication with Creative Director
     ],
     shared_instructions='./agency_manifesto.md',  # shared instructions for all agents
     temperature=0.3,  # default temperature for all agents
     max_prompt_tokens=10000,  # reduced max tokens to prevent timeout issues
     )

# Start email monitoring
agency.start_email_monitoring()
logger.info("Agency setup completed")

if __name__ == '__main__':
    logger.info("Starting Gradio demo...")
    agency.demo_gradio()