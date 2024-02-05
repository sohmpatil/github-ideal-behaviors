import requests


def get_collaborators(repo_owner, repo_name, access_token):

    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators'
    headers = {
        'Authorization': f'token {access_token}'
    }
    response = requests.get(api_url, headers=headers)

    collaborators = []
    if response.status_code == 200:
        collaborators_response = response.json()
        for collaborator in collaborators_response:
            collaborators.append(collaborator['login'])
        return collaborators
    else:
        print(f"Error: {response.status_code}")
        return collaborators
