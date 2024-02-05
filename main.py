import os

from utils.collaborators import get_collaborators


if __name__ == '__main__':
    repository_owner = 'asu-cse578-s2023'
    repository_name = 'Anisha-Roshan-Sanika-Sanket-Sarthak-Soham'

    # Set git access token in env
    access_token = os.environ.get('git_access_token')

    developers = get_collaborators(
        repository_owner, repository_name, access_token)

    if developers:
        print(f"List of Developers to {repository_owner}/{repository_name}:")
        for developer in developers:
            print(f"{developers}")
    else:
        print("Unable to retrieve developers.")
