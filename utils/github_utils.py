import requests
import os
import collections


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

def get_changed_files(owner, repo, commit_sha, access_token):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code ==  200:
        commit_data = response.json()
        files = commit_data.get('files', [])
        changed_files = [os.path.splitext(file['filename'])[1] for file in files]
        changed_files_extension = collections.Counter(changed_files)
        return changed_files_extension
    else:
        print(f"Error: {response.status_code}")
        return {}


def get_number_of_new_lines(owner, repo, commit_sha, access_token):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_data = response.json()
        print("Commit ID: ", commit_sha)
        lines = commit_data.get('stats', [])
        additions = lines.get('additions', 0)
        deletions = lines.get('deletions', 0)

        print(f"No. of New lines added: {additions}")
        print(f"No. of lines deleted: {deletions}")

    else:
        print(f"Error: {response.status_code}")
        return {}