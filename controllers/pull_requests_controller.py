import requests
import logging


from models.pull_requests_model import PullRequestsList, PullRequests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pull_requests_contoller")


def get_pull_requests(repo_owner, repo_name, access_token):
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
