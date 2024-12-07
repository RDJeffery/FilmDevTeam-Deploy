from agency_swarm.agents import Agent
from FilmDevAgency.common_tools.WhatsAppTool import WhatsAppTool
from FilmDevAgency.common_tools.ScriptNotepadTool import ScriptNotepadTool


class CreativeDirector(Agent):
    def __init__(self, name="Creative Director"):
        super().__init__(
            name=name,
            description="The Creative Director serves as the main liaison point, coordinating all tasks in the workflow and ensuring alignment with the unified vision. Can communicate via WhatsApp and manage script notes.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[WhatsAppTool, ScriptNotepadTool],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        return message
