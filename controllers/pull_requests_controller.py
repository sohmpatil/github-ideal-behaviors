import requests
import logging

from models.pull_requests_model import PullRequestsList, PullRequests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pull_requests_contoller")


def get_pull_requests(repo_owner: str, repo_name: str, access_token: str, requests=requests) -> PullRequestsList:
    """
        Retrieve a list of pull requests from a GitHub repository.

        Args:
            repo_owner (str): The owner of the GitHub repository.
            repo_name (str): The name of the GitHub repository.
            access_token (str): The personal access token used for authentication.
            requests (Optional[module]): The `requests` module to use for making HTTP requests.
            Defaults to the `requests` module if not provided explicitly.

        Returns:
            PullRequestsList: A list of pull requests from the specified repository.

        Raises:
            None.
    """
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls?state=all'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        pr_response = response.json()
        pull_requests = PullRequestsList(
            pull_requests=[PullRequests.parse_obj(pr) for pr in pr_response])
        return pull_requests

    else:
        log.error(f"Error: {response.status_code}")
        return PullRequestsList(pull_requests=[])
