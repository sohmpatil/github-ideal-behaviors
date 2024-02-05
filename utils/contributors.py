import requests


def get_contributors(repo_owner, repo_name, access_token):

    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contributors'
    headers = {
        'Authorization': f'token {access_token}'
    }
    response = requests.get(api_url, headers=headers)

    contributors = []
    if response.status_code == 200:
        contributors_response = response.json()
        for contributor in contributors_response:
            contributors.append(contributor['login'])
        return contributors
    else:
        print(f"Error: {response.status_code}")
        return contributors
