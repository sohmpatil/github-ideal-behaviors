import requests
import logging

from models.commits_model import CommitsList

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("commits_controller")


def get_commits(owner: str, repo: str, access_token: str, author: str = '', requests=requests) -> CommitsList:
    """
        Retrieve a list of commits from a GitHub repository.

        Args:
            owner (str): The owner of the GitHub repository.
            repo (str): The name of the GitHub repository.
            access_token (str): The personal access token used for authentication.
            requests (Optional[module]): The `requests` module to use for making HTTP requests.
            Defaults to the `requests` module if not provided explicitly.

        Returns:
            CommitsList: A list of commits from the specified repository.

        Raises:
            None.
    """

    page = 1
    commits = CommitsList(commits=[])

    while True:
        api_url = f'https://api.github.com/repos/{owner}/{repo}/commits?per_page=100&page={page}'
        if author != '':
            api_url += f'&author={author}'
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            commits_response = response.json()
            if not commits_response:
                break
            new_commits = CommitsList(commits=commits_response)
            commits.commits.extend(new_commits.commits)
            page += 1
        else:
            log.error(f"Error: {response.status_code}")
            return commits

    return commits
