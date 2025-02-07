import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


class BitbucketClient:
    def __init__(self):
        """
        Initialize the client with authentication and repository details.

        :param username: Bitbucket username.
        :param app_password: Bitbucket app password.
        :param workspace: The workspace ID (or team name).
        :param repo_slug: The repository slug.
        """

        BITBUCKET_USERNAME = os.getenv('BITBUCKET_USERNAME')
        BITBUCKET_APP_PASSWORD = os.getenv('BITBUCKET_APP_PASSWORD')

        self.username = BITBUCKET_USERNAME
        self.auth = HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD)
        self.workspace = os.getenv('BITBUCKET_WORKSPACE')
        self.repo_slug = os.getenv('BITBUCKET_REPO_SLUG')
        self.base_url = "https://api.bitbucket.org/2.0"  # For Bitbucket Cloud

    def _build_url(self, path):
        """Helper to build a full URL for the API call."""
        return f"{self.base_url}{path}"

    def get_open_pull_requests(self, repo_slug: str):
        """
        Retrieve a list of open pull requests.
        """
        url = self._build_url(f"/repositories/{self.workspace}/{repo_slug}/pullrequests")
        params = {'state': 'OPEN'}
        response = requests.get(url, params=params, auth=self.auth)
        response.raise_for_status()
        data = response.json()
        return data.get('values', [])

    def get_pull_request_details(self, repo_slug: str, pull_request_id: int):
        """
        Retrieve detailed information for a specific pull request, including its description and branches.

        param pull_request_id: The ID of the pull request.
        return: A JSON object with pull request details.
        """
        url = self._build_url(f"/repositories/{self.workspace}/{repo_slug}/pullrequests/{pull_request_id}")
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def get_pull_request_diff(self, repo_slug: str, pull_request_id: int):
        """
        Retrieve the full diff for a given pull request.
        Alternatively, you could use `/diffstat` if you want a summary.
        """
        url = self._build_url(f"/repositories/{self.workspace}/{repo_slug}/pullrequests/{pull_request_id}/diff")
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        # The diff is returned as plain text.
        return response.text

    def comment_on_file_in_pull_request(self, repo_slug: str, pull_request_id: int, content, file_path, line_number):
        """
        Post a comment on a pull request with an inline annotation.

        :param pull_request_id: The ID of the pull request.
        :param content: The text of the comment.
        :param file_path: The path to the file you wish to comment on.
        :param line_number: The line number to attach the comment. This is usually specified using 'to' (or 'from' if applicable).
        """
        url = self._build_url(
            f"/repositories/{self.workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments")
        payload = {
            "content": {
                "raw": content
            },
            "inline": {
                "path": file_path,
                "to": line_number
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def comment_on_pull_request(self, repo_slug: str, pull_request_id: int, content):
        """
        Post a comment on a pull request with an inline annotation.

        :param pull_request_id: The ID of the pull request.
        :param content: The text of the comment.
        """
        url = self._build_url(
            f"/repositories/{self.workspace}/{repo_slug}/pullrequests/{pull_request_id}/comments")
        payload = {
            "content": {
                "raw": content
            },
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def get_file_contents(self, file_path: str, repo_slug: str, ref: str = None) -> str:
        """
        Retrieve the contents of a file from the repository.

        param file_path: The path to the file within the repository.
        param ref: Optional branch name, commit hash, or tag. If not provided,
                    the default branch is used.
        return: The content of the file as a string.
        """
        # Construct the URL. If ref is provided, include it; otherwise, omit.
        if ref:
            url = self._build_url(f"/repositories/{self.workspace}/{repo_slug}/src/{ref}/{file_path}")
        else:
            url = self._build_url(f"/repositories/{self.workspace}/{repo_slug}/src/{file_path}")

        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.text


# Example usage:
if __name__ == "__main__":

    # Load environment variables from .env file
    load_dotenv()

    client = BitbucketClient()

    # 1. Retrieve open pull requests.
    try:
        prs = client.get_open_pull_requests("game-of-life")
        print("Open Pull Requests:")
        for pr in prs:
            print(f"ID: {pr['id']}, Title: {pr['title']}")
    except Exception as e:
        print("Error fetching pull requests:", e)

    try:
        comment_response = client.comment_on_pull_request(
            repo_slug="game-of-life",
            pull_request_id=3,
            content="This is a comment on the code at a specific line.",
            file_path="src/README.md",  # Adjust this path to one present in the diff.
            line_number=1  # The line number you wish to comment on.
        )
        print("\nComment posted:")
        print(comment_response)
    except Exception as e:
        print("Error posting comment:", e)

    # # 2. Retrieve the diff for a specific pull request (choose one from the list)
    # if prs:
    #     pr_id = prs[0]['id']
    #     try:
    #         diff = client.get_pull_request_diff(pr_id)
    #         print(f"\nDiff for Pull Request {pr_id}:")
    #         print(diff)
    #     except Exception as e:
    #         print("Error fetching pull request diff:", e)
    #
    #     # 3. Post an inline comment on a specific file and line.
    #     try:
    #         comment_response = client.comment_on_pull_request(
    #             pull_request_id=pr_id,
    #             content="This is a comment on the code at a specific line.",
    #             file_path="src/example.py",  # Adjust this path to one present in the diff.
    #             line_number=42  # The line number you wish to comment on.
    #         )
    #         print("\nComment posted:")
    #         print(comment_response)
    #     except Exception as e:
    #         print("Error posting comment:", e)