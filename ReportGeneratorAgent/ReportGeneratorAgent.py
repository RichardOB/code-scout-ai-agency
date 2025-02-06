from agency_swarm.agents import Agent


class ReportGeneratorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ReportGeneratorAgent",
            description="The Report Generator agent compiles a report based on the analysis provided by the Code Analyzer agent and prepares it for the user.",
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
