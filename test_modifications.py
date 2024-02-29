import os
import utils.github_utils as git_utils

repository_name = 'Anisha-Roshan-Sanika-Sanket-Sarthak-Soham'
repository_owner = 'asu-cse578-s2023'

access_token = "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"

commits = git_utils.get_commits(
    repository_owner,
    repository_name,
    access_token,
    ''
)

collaborators = git_utils.get_collaborators(repository_owner,repository_name,access_token)

for commit in commits:
    print("commit: ")
    print(commit)
print("collaborators: ", collaborators)

