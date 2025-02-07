from agency_swarm.tools import BaseTool
from pydantic import Field

from clients.bitbucket_client import BitbucketClient


class BitbucketAddGeneralCommentToPullRequestTool(BaseTool):
    """
    This tool interfaces with the Bitbucket API to add a general comment to a pull request.
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

    def run(self):
        """
        Executes the tool's main functionality: Adding a comment to a Bitbucket pull request.
        """

        client = BitbucketClient()

        try:
            comment_response = client.comment_on_pull_request(
                repo_slug=self.repository_slug,
                pull_request_id=self.pull_request_id,
                content=self.comment_content
            )

            return {
                "comment_response": comment_response
            }
        
        except Exception as e:
            print("Error posting comment:", e)

