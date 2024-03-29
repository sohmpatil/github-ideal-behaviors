import requests
import logging

from models.commit_details_model import CommitDetail
from typing import Optional

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("commits_details_controller")


def get_commit_details(owner, repo, commit_sha, access_token, requests=requests) -> Optional[CommitDetail]:
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
