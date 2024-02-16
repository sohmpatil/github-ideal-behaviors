import os
import utils.github_utils as git_utils

repository_owner = 'sanket8397'
repository_name = 'CSE_564_Assignment_3_4'

access_token = os.environ.get('git_access_token')

print(access_token)

commits = git_utils.get_commits(
    repository_owner,
    repository_name,
    access_token,
    'sanket8397'
)

print(commits)
