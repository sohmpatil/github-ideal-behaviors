import requests
from models.commits_model import CommitsList
def get_commits(owner, repo, access_token, author=''):
    page = 1
    commits = []

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
            commits = CommitsList(commits=commits_response)
            page += 1
        else:
            print(f"Error: {response.status_code}")
            return []

    return commits