import requests
import logging

from models.commits_model import CommitsList

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("commits_controller")


def get_commits(owner, repo, access_token, author='', requests=requests) -> CommitsList:
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
