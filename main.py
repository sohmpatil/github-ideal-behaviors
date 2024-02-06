import os

import utils.github_utils as git_utils


if __name__ == '__main__':
    repository_owner = 'asu-cse578-s2023'
    repository_name = 'Anisha-Roshan-Sanika-Sanket-Sarthak-Soham'

    # Set git access token in env
    access_token = os.environ.get('git_access_token')

    developers = git_utils.get_collaborators(
        repository_owner, repository_name, access_token)

    if developers:
        print(f"List of Developers to {repository_owner}/{repository_name}:")
        for developer in developers:
            print(f"{developer}")
    else:
        print("Unable to retrieve developers.")

    commits = git_utils.get_commits(repository_owner, repository_name, access_token)

    if commits:
        print(f"Commits List of {repository_owner}/{repository_name}:")
        for commit in commits:
            print(git_utils.get_changed_files(repository_owner, repository_name, commit, access_token))
    else:
        print("No commits found.")
