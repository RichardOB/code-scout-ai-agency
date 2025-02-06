from agency_swarm.agents import Agent


class CEOAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CEOAgent",
            description="The CEO agent acts as the primary communicator and coordinator for the CodeScoutAgency. It communicates with the user and the Code Analyzer agent to ensure the task is completed efficiently. The CEO agent will use the Bitbucket API for overseeing the process.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        return message
