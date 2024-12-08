from agency_swarm.agents import Agent
from FilmDevAgency.common_tools.ScriptNotepadTool import ScriptNotepadTool
from FilmDevAgency.common_tools.EmailTool import ScriptNotepadEmailTool
import logging

# Configure logging
logger = logging.getLogger(__name__)

class CreativeDirector(Agent):
    def __init__(self, name="Creative Director"):
        super().__init__(
            name=name,
            description="The Creative Director serves as the main liaison point, coordinating all tasks in the workflow and ensuring alignment with the unified vision. Can communicate via Telegram and email with a witty personality, and manage script notes.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[ScriptNotepadTool, ScriptNotepadEmailTool],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        logger.info("Creative Director initialized")

    def response_validator(self, message):
        return message
