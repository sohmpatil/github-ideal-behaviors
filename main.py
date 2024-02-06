import os

import utils.github_utils as git_utils

repository_owner = 'asu-cse578-s2023'
repository_name = 'Anisha-Roshan-Sanika-Sanket-Sarthak-Soham'

# Set git access token in env
access_token = os.environ.get('git_access_token')

# Get number of commits for each developer


def get_dev_commits():
    dev_commits = {}
    developers = git_utils.get_collaborators(
        repository_owner, repository_name, access_token)

    if developers:
        for developer in developers:
            commits = git_utils.get_commits(
                repository_owner, repository_name, access_token, developer)
            # print(f"{developer}, {len(commits)}")
            dev_commits[developer] = len(commits)
    else:
        print("Unable to retrieve developers.")

    return dev_commits


if __name__ == '__main__':

    dev_commits = get_dev_commits()
    print(dev_commits)

    commits = git_utils.get_commits(
        repository_owner, repository_name, access_token)
    print(commits)
    if commits:
        print(f"Commits List of {repository_owner}/{repository_name}:")
        for commit in commits:
            files_extension_dict = git_utils.get_changed_files(repository_owner,
                                                               repository_name,
                                                               commit,
                                                               access_token)
            print(f"Commit ID: {commit}")
            print(f"Extension Counts {dict(files_extension_dict)}")
            print(f"Total changed files in the commit: {
                  sum(files_extension_dict.values())}")
    else:
        print("No commits found.")

    if commits:
        print(f"Commits List of {repository_owner}/{repository_name}:")
        for commit in commits:
            git_utils.get_number_of_new_lines(
                repository_owner, repository_name, commit, access_token)
    else:
        print("No commits found.")
    collaborators = git_utils.get_collaborators(
        repository_owner, repository_name, access_token)
    for collaborator in collaborators:
        print(f"Time difference in consecutive commits for {collaborator}")
        time_diffs = git_utils.fetch_consecutime_time_between_commits(
            repository_owner, repository_name, access_token, collaborator)
        print(time_diffs)
