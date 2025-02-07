from agency_swarm.tools import BaseTool
from pydantic import Field

from clients.bitbucket_client import BitbucketClient


class BitbucketAddCommentToFileTool(BaseTool):
    """
    This tool interfaces with the Bitbucket API to add a comment to a file on a specific line within a specific pull request.
    """

    comment_content: str = Field(
        ..., description="The comment to add to the pull request"
    )
    repository_slug: str = Field(
        ..., description="The slug of the repository for which to list pull requests."
    )
    pull_request_id: int = Field(
        ..., description="The ID of the pull request to fetch details for, including code changes."
    )
    file_path: str = Field(
        ..., description="The path to the file within the repository"
    )
    line_number: int = Field(
        ..., description="The line number of the file to add the comment to"
    )

    def run(self):
        """
        Executes the tool's main functionality: Adding a comment to a line of a file in a Bitbucket pull request.
        """

        client = BitbucketClient()

        try:
            comment_response = client.comment_on_file_in_pull_request(
                repo_slug=self.repository_slug,
                pull_request_id=self.pull_request_id,
                content=self.comment_content,
                file_path=self.file_path,
                line_number=self.line_number
            )

            return {
                "comment_response": comment_response
            }

        except Exception as e:
            print("Error posting comment:", e)

