import requests
import logging

from models.collaborators_model import CollaboratorsList

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("collaborators_contoller")


def get_collaborators(repo_owner, repo_name, access_token, requests=requests) -> CollaboratorsList:
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
