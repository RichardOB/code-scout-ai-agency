from agency_swarm.tools import BaseTool
from pydantic import Field

from clients.bitbucket_client import BitbucketClient


class BitbucketGetPullRequestDiffTool(BaseTool):
    """
    This tool interfaces with the Bitbucket API to retrieve the diff string for a pull request.
    """

    repository_slug: str = Field(
        ..., description="The slug of the repository for which to list pull requests."
    )
    pull_request_id: int = Field(
        None, description="The ID of the pull request to fetch details for, including code changes."
    )

    def run(self):
        """
        Executes the tool's main functionality: listing pull requests or fetching details of a specific pull request.
        """

        client = BitbucketClient()

        if self.pull_request_id is None:
            # List pull requests for the given repository
            pull_requests = client.get_open_pull_requests(repo_slug=self.repository_slug)
            return pull_requests
        else:
            # Fetch details of a specific pull request
            pull_request_details = client.get_pull_request_details(
                repo_slug=self.repository_slug,
                pull_request_id=self.pull_request_id
            )

            # Fetch code changes for the specific pull request
            code_changes = client.get_pull_request_diff(
                repo_slug=self.repository_slug,
                pull_request_id=self.pull_request_id
            )

            return {
                "pull_request_details": pull_request_details,
                "code_changes": code_changes
            }


# if __name__ == "__main__":
#     tool = BitbucketGetPullRequestDiffTool(repository_slug='chatbot-service', pull_request_id=609)
#     tool.pull_request_id = 609
#     tool.repository_slug = 'chatbot-service'
#     print(tool.run())