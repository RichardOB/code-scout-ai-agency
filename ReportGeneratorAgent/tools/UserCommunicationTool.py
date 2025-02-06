from agency_swarm.tools import BaseTool
from pydantic import Field

class UserCommunicationTool(BaseTool):
    """
    This tool prepares the compiled report for the user.
    It formats the report for presentation, ensuring clarity and accessibility,
    and delivers it to the user through the appropriate channel.
    """

    compiled_report: str = Field(
        ..., description="The compiled report to be formatted and delivered to the user."
    )
    user_contact_info: str = Field(
        ..., description="The contact information of the user to whom the report will be delivered."
    )

    def run(self):
        """
        Executes the tool's main functionality: formatting the compiled report for presentation
        and delivering it to the user.
        """
        # Format the compiled report for presentation
        formatted_report = self.format_report_for_presentation(self.compiled_report)

        # Deliver the formatted report to the user
        self.deliver_report_to_user(formatted_report, self.user_contact_info)

        return "Report formatted and delivered to the user."

    def format_report_for_presentation(self, report):
        """
        Formats the compiled report for presentation, ensuring clarity and accessibility.
        """
        # Example of formatting logic (this can be customized as needed)
        formatted_report = f"*** User-Friendly Report ***\n\n{report}\n\n*** End of Report ***"
        return formatted_report

    def deliver_report_to_user(self, report, contact_info):
        """
        Delivers the formatted report to the user through the appropriate channel.
        This is a placeholder for the actual delivery mechanism.
        """
        # Example of delivery logic (this should be replaced with actual delivery logic)
        # For example, sending an email or a message
        print(f"Delivering report to user at {contact_info}:\n{report}")