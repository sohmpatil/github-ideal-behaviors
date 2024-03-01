import requests
from models.commit_details_model import CommitDetail

def get_commit_details(owner, repo, commit_sha, access_token):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_response = response.json()
        commit_details = {}
        commit_details = CommitDetail(**commit_response)
        return commit_details
    else:
        return None
