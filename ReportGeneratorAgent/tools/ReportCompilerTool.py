from agency_swarm.tools import BaseTool
from pydantic import Field

class ReportCompilerTool(BaseTool):
    """
    This tool compiles reports based on the analysis findings received.
    It formats the data into a user-friendly report, highlighting key insights and recommendations.
    """

    analysis_data: str = Field(
        ..., description="The analysis findings data to be compiled into a report."
    )

    def run(self):
        """
        Executes the tool's main functionality: compiling the analysis data into a user-friendly report.
        """
        # Compile the analysis data into a report
        report = self.compile_report(self.analysis_data)

        return report

    def compile_report(self, data):
        """
        Compiles the analysis data into a user-friendly report.
        """
        # Example of report compilation logic
        # This can be customized to include specific formatting, insights, and recommendations
        report_header = "Code Analysis Report\n"
        report_header += "=" * 20 + "\n\n"

        insights = "Key Insights:\n"
        insights += "- Review the highlighted issues for potential improvements.\n"
        insights += "- Consider refactoring complex code sections.\n\n"

        recommendations = "Recommendations:\n"
        recommendations += "- Follow coding standards to improve code quality.\n"
        recommendations += "- Use automated tools for continuous code quality checks.\n\n"

        report_body = f"Analysis Findings:\n{data}\n\n"

        # Combine all parts into the final report
        full_report = report_header + insights + recommendations + report_body

        return full_report