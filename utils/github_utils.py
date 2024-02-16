import datetime
import requests
import os
import collections
import logging

from .comments_utils import getuncommentedLines

# Setup logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("github_utils")


def get_collaborators(repo_owner, repo_name, access_token):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)

    collaborators = []
    if response.status_code == 200:
        collaborators_response = response.json()
        for collaborator in collaborators_response:
            collaborators.append(collaborator['login'])
        return collaborators
    else:
        log.error(f"Error: {response.status_code}")
        return collaborators


def get_commits(owner, repo, access_token, author=''):
    api_url = f'https://api.github.com/repos/{owner}/{repo}/commits?per_page=100'
    if author != '':
        api_url += f'&author={author}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        commits = response.json()
        commit_shas = [commit['sha'] for commit in commits]
        return commit_shas
    else:
        log.error(f"Error: {response.status_code}")
        return []


def get_changed_files(owner, repo, commit_sha, access_token):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_data = response.json()
        files = commit_data.get('files', [])
        changed_files = [
            os.path.splitext(file['filename'])[1]
            for file in files
        ]
        changed_files_extension = collections.Counter(changed_files)
        return changed_files_extension
    else:
        log.error(f"Error: {response.status_code}")
        return {}


def get_number_of_new_lines(owner, repo, commit_sha, access_token):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_data = response.json()
        log.info(f"Commit ID: {commit_sha}")
        lines = commit_data.get('stats', [])
        additions = lines.get('additions', 0)
        deletions = lines.get('deletions', 0)

        log.info(f"No. of New lines added: {additions}")
        log.info(f"No. of lines deleted: {deletions}")
    else:
        log.error(f"Error: {response.status_code}")
        return {}


def fetch_consecutive_time_between_commits(repo_owner, repo_name, access_token, author):
    commits = get_commits(
        repo_owner,
        repo_name,
        access_token,
        author=author
    )
    timestamp_list = []
    for sha in commits:
        commit_timestamp = get_commit_timestamp(
            repo_owner,
            repo_name,
            sha,
            access_token
        )
        timestamp_list.append(commit_timestamp)
    if timestamp_list:
        time_diffs = calculate_time_diffs(timestamp_list)
        return time_diffs
    else:
        log.info("No commits found.")


def get_commit_timestamp(owner, repo, commit_sha, access_token):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_data = response.json()
        timestamp = commit_data['commit']['author'].get('date')
        return timestamp
    else:
        log.error(f"Error: {response.status_code}")
        return None


def calculate_time_diffs(timestamp_list):
    log.info(timestamp_list)
    # Convert strings to datetime objects
    timestamps = [
        datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        for ts in timestamp_list[::-1]
    ]
    # Calculate time differences in hours
    time_diffs = [
        (timestamps[i+1] - timestamps[i]).total_seconds() / 3600
        for i in range(len(timestamps)-1)
    ]
    return time_diffs


def get_added_lines(owner, repo, commit_sha, access_token):
    """
        function returns dictionary with file name as key and lines added as values
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_info = response.json()
        added_lines = dict()
        files_changed = commit_info['files']
        for file in files_changed:
            if file['status'] == 'added':
                file_url = file['raw_url']
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    added_lines[file['filename']] = file_response.text
                else:
                    log.error(f"Failed to retrieve file content: {file_url}")
        return added_lines
    else:
        log.error(f"Error: {response.status_code}")
        return None


def getmeaningfulLines(owner, repo, commit_sha, access_token):
    files_changed = get_added_lines(owner, repo, commit_sha, access_token)
    meaningfulLines = 0
    for file_name, content in files_changed.items():
        meaningfulLines += getuncommentedLines(
            file_name, content)
    return meaningfulLines
