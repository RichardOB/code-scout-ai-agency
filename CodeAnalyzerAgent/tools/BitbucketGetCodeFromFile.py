from agency_swarm.tools import BaseTool
from pydantic import Field

from clients.bitbucket_client import BitbucketClient


class BitbucketGetGetCodeFromFileTool(BaseTool):
    """
    This tool interfaces with the Bitbucket API to retrieve the contents of a file in a specific branch or commit.
    """

    repository_slug: str = Field(
        ..., description="The slug of the repository for which to list pull requests."
    )
    source_branch_name: str = Field(
        ..., description="The name of the src branch or the latest commit hash"
    )
    file_path: str = Field(
        ..., description="The path to the file within the repository"
    )


    def run(self):
        """
        Executes the tool's main functionality: listing pull requests or fetching details of a specific pull request.
        """

        client = BitbucketClient()

        file_contents = client.get_file_contents(
            file_path=self.file_path,
            ref=self.source_branch_name,
            repo_slug=self.repository_slug
        )

        return {
            "file_path": self.file_path,
            "file_contents": file_contents
        }


if __name__ == "__main__":
    # tool = BitbucketGetGetCodeFromFileTool(
    #     repository_slug='chatbot-service',
    #     source_branch_name='development',
    #     file_path='chatbot_service/database/models/employee_notification_model.py'
    # )
    tool = BitbucketGetGetCodeFromFileTool(
        repository_slug='game-of-life',
        source_branch_name='feature/basic-setup',
        file_path='app/models.py'
    )
    print(tool.run())