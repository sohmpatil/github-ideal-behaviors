import os
import logging
import utils.github_utils as git_utils

repository_owner = 'asu-cse578-s2023'
repository_name = 'Anisha-Roshan-Sanika-Sanket-Sarthak-Soham'

# Set up logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")
# Set git access token in env
access_token = os.environ.get('git_access_token')


def get_dev_commits():
    """Get number of commits for each developer"""
    dev_commits = {}
    developers = git_utils.get_collaborators(
        repository_owner, 
        repository_name, 
        access_token
    )
    if not developers:
        return {}

    for developer in developers:
        commits = git_utils.get_commits(
            repository_owner, 
            repository_name, 
            access_token, 
            developer
        )
        dev_commits[developer] = len(commits)

    return dev_commits


if __name__ == '__main__':
    dev_commits = get_dev_commits()
    log.info(dev_commits)

    commits = git_utils.get_commits(
        repository_owner, 
        repository_name, 
        access_token
    )
    log.info(commits)
    if commits:
        log.info(f"Commits List of {repository_owner}/{repository_name}:")
        for commit in commits:
            files_extension_dict = git_utils.get_changed_files(
                repository_owner,
                repository_name,
                commit,
                access_token
            )
            log.info(f"Commit ID: {commit}")
            log.info(f"Extension Counts {dict(files_extension_dict)}")
            log.info(f"Total changed files in the commit: \
                     {sum(files_extension_dict.values())}")
    else:
        log.info("No commits found.")

    if commits:
        log.info(f"Commits List of {repository_owner}/{repository_name}:")
        for commit in commits:
            git_utils.get_number_of_new_lines(
                repository_owner, 
                repository_name, 
                commit, 
                access_token
            )
    else:
        log.info("No commits found.")

    collaborators = git_utils.get_collaborators(
        repository_owner, repository_name, access_token)
    for collaborator in collaborators:
        log.info(f"Time difference in consecutive commits for {collaborator}")
        time_diffs = git_utils.fetch_consecutive_time_between_commits(
            repository_owner, 
            repository_name, 
            access_token, 
            collaborator
        )
        log.info(time_diffs)
