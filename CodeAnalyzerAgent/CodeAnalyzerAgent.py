from agency_swarm.agents import Agent

from CodeAnalyzerAgent.tools.BitbucketGetCodeFromFile import BitbucketGetGetCodeFromFileTool
from CodeAnalyzerAgent.tools.BitbucketGetPullRequestDiffTool import BitbucketGetPullRequestDiffTool
from CodeAnalyzerAgent.tools.GetListOfChangedFilesFromDiff import GetListOfChangedFilesFromDiff


class CodeAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CodeAnalyzerAgent",
            description="The Code Analyzer agent retrieves changes from pull requests using the Bitbucket API, fetches complete files from Bitbucket API if needed, and analyse each file or code change before suggesting pytest unit tests that can be created.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[BitbucketGetGetCodeFromFileTool, BitbucketGetPullRequestDiffTool, GetListOfChangedFilesFromDiff],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        return message
