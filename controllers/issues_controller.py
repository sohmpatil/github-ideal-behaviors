import requests
import logging

from models.issues_model import IssueList

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("issues_contoller")


def get_issues(repo_owner: str, repo_name: str, access_token: str, requests=requests) -> IssueList:
    """
        Retrieve a list of issues from a GitHub repository.

        Args:
            repo_owner (str): The owner of the GitHub repository.
            repo_name (str): The name of the GitHub repository.
            access_token (str): The personal access token used for authentication.
            requests (Optional[module]): The `requests` module to use for making HTTP requests.
            Defaults to the `requests` module if not provided explicitly.

        Returns:
            IssueList: A list of issues from the specified repository.

        Raises:
            None.
    """
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        issues_response = response.json()
        issues = IssueList(issues=issues_response)
        return issues
    else:
        log.error(f"Error: {response.status_code}")
        return IssueList(issues=[])
