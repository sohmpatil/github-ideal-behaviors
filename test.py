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

# print(commits)
commit = 'a2b7614801e2a3707bbc4702b98845de5ffa0169'
# commit = 'b49812fb1d9226f18d572849c165230a144ef4ef'
n = git_utils.get_meaningful_lines(
    repository_owner, repository_name, commit, access_token)
print(n)
