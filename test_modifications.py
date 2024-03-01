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

commit = 'd05c4839a01fad8ee49102a7e531942fd6612faf'
# commit = 'b49812fb1d9226f18d572849c165230a144ef4ef'
n = git_utils.get_meaningful_lines(
    repository_owner, repository_name, commit, access_token)
print("meaningful lines: ", n)


commit = 'd05c4839a01fad8ee49102a7e531942fd6612faf'
# commit = 'b49812fb1d9226f18d572849c165230a144ef4ef'
changed_files = git_utils.get_changed_files(
    repository_owner, repository_name, commit, access_token)
print("changed files: ", changed_files)


additions, deletions = git_utils.get_number_of_new_lines(
    repository_owner, repository_name, commit, access_token)
print("Additons: ", additions)
print("Deletion: ", deletions)


timestamp = git_utils.get_commit_timestamp(
    repository_owner, repository_name, commit, access_token)
print("timestamp : ", timestamp)
