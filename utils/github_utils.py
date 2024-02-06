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

def get_commits(owner, repo, access_token):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits?sha=main'
    headers = {'Authorization': f'token {access_token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code ==  200:
        commits = response.json()
        commit_shas = [commit['sha'] for commit in commits]
        return commit_shas
    else:
        print(f"Error: {response.status_code}")
        return []
