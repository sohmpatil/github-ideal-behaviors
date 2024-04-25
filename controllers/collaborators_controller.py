import requests
import logging

from models.collaborators_model import CollaboratorsList

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("collaborators_contoller")


def get_collaborators(repo_owner: str, repo_name: str, access_token: str, requests=requests) -> CollaboratorsList:
    """
    Retrieve a list of collaborators for a GitHub repository.

    Args:
        repo_owner (str): The owner of the GitHub repository.
        repo_name (str): The name of the GitHub repository.
        access_token (str): The personal access token used for authentication.
        requests (Optional[module]): The `requests` module to use for making HTTP requests.
            Defaults to the `requests` module if not provided explicitly.

    Returns:
        CollaboratorsList: A list of collaborators for the specified repository.

    Raises:
        None.
    """
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        collaborators_response = response.json()
        collaborators = CollaboratorsList(collaborators=collaborators_response)
        return collaborators
    else:
        log.error(f"Error: {response.status_code}")
        return CollaboratorsList(collaborators=[])
