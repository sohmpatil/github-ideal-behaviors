import requests
import logging

from models.issues_model import IssueList

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("issues_contoller")


def get_issues(repo_owner, repo_name, access_token):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        issues_response = response.json()
        issues = IssueList(issues=issues_response)
        return issues
    else:
        log.error(f"Error: {response.status_code}")
        return []
