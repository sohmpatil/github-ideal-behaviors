import requests
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pull_requests_contoller")


def get_pull_requests(repo_owner, repo_name, access_token):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls?state=all'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        pr_response = response.json()
        for pr in pr_response:
            print(pr['id'], pr['user']['login'], pr['assignee'], pr['assignees'],
                  pr['created_at'], pr['closed_at'])
            if len(pr['assignees']) == 1:
                pprint(pr)
        return pr_response
    else:
        log.error(f"Error: {response.status_code}")
        return []
