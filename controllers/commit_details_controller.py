import requests
import logging

from models.commit_details_model import CommitDetail
from typing import Optional

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("commits_details_controller")


def get_commit_details(owner: str, repo: str, commit_sha: str, access_token: str, requests=requests) -> Optional[CommitDetail]:
    """
        Retrieve details of a specific commit from a GitHub repository.

        Args:
            owner (str): The owner of the GitHub repository.
            repo (str): The name of the GitHub repository.
            commit_sha (str): The SHA hash of the commit to retrieve details for.
            access_token (str): The personal access token used for authentication.
            requests (Optional[module]): The `requests` module to use for making HTTP requests.
            Defaults to the `requests` module if not provided explicitly.

        Returns:
            Optional[CommitDetail]: Details of the specified commit if found, or None if the commit is not found or an error occurs.

        Raises:
            None.
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_response = response.json()
        commit_details = {}
        commit_details = CommitDetail(**commit_response)
        return commit_details
    else:
        log.error(f"Error: {response.status_code}")
        return None
