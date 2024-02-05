import os

from utils.contributors import get_contributors

if __name__ == '__main__':
    repository_owner = 'asu-cse578-s2023'
    repository_name = 'Anisha-Roshan-Sanika-Sanket-Sarthak-Soham'

    # Set git access token in env
    access_token = os.environ.get('git_access_token')

    contributors = get_contributors(
        repository_owner, repository_name, access_token)

    if contributors:
        print(f"List of Contributors to {repository_owner}/{repository_name}:")
        for contributor in contributors:
            print(f"{contributor}")
    else:
        print("Unable to retrieve contributors.")
