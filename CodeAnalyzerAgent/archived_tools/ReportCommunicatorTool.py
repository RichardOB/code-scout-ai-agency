from agency_swarm.tools import BaseTool
from pydantic import Field

class ReportCommunicatorTool(BaseTool):
    """
    This tool communicates the findings of the code analysis to the Report Generator agent.
    It formats the analysis results into a structured message and sends it to the Report Generator agent
    for further processing.
    """

    analysis_results: str = Field(
        ..., description="The results of the code analysis to be communicated."
    )
    report_generator_agent_id: str = Field(
        ..., description="The identifier of the Report Generator agent to send the message to."
    )

    def run(self):
        """
        Executes the tool's main functionality: formatting the analysis results and sending them
        to the Report Generator agent.
        """
        # Format the analysis results into a structured message
        structured_message = self.format_analysis_results(self.analysis_results)

        # Send the structured message to the Report Generator agent
        self.send_to_report_generator(structured_message, self.report_generator_agent_id)

        return f"Analysis results sent to Report Generator agent {self.report_generator_agent_id}"

    def format_analysis_results(self, results):
        """
        Formats the analysis results into a structured message.
        """
        # Example of formatting the results (this can be customized as needed)
        formatted_results = f"Code Analysis Report:\n\n{results}"
        return formatted_results

    def send_to_report_generator(self, message, agent_id):
        """
        Sends the formatted message to the Report Generator agent.
        This is a placeholder for the actual communication mechanism.
        """
        # Example of sending the message (this should be replaced with actual communication logic)
        # For example, using a messaging system or shared state
        print(f"Sending message to agent {agent_id}: {message}")