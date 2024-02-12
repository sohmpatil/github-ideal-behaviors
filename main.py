from fastapi import FastAPI
import logging
import utils.github_utils as git_utils

app = FastAPI()


# Set up logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

@app.get("/analyze")
async def analyze_repository(repository_owner: str, repository_name: str, git_access_token: str):
    dev_commits = get_dev_commits(repository_owner, repository_name, git_access_token)
    log.info(dev_commits)

    commits = git_utils.get_commits(
        repository_owner,  
        repository_name,  
        git_access_token
    )
    log.info(commits)
    if commits:
        log.info(f"Commits List of {repository_owner}/{repository_name}:")
        for commit in commits:
            files_extension_dict = git_utils.get_changed_files(
                repository_owner,
                repository_name,
                commit,
                git_access_token
            )
            log.info(f"Commit ID: {commit}")
            log.info(f"Extension Counts {dict(files_extension_dict)}")
            log.info(f"Total changed files in the commit: \
                     {sum(files_extension_dict.values())}")
    else:
        log.info("No commits found.")

    collaborators = git_utils.get_collaborators(
        repository_owner, repository_name, git_access_token)
    for collaborator in collaborators:
        log.info(f"Time difference in consecutive commits for {collaborator}")
        time_diffs = git_utils.fetch_consecutive_time_between_commits(
            repository_owner,  
            repository_name,  
            git_access_token,  
            collaborator
        )
        log.info(time_diffs)

    # Return the results
    return {
        "dev_commits": dev_commits,
        "commits": commits,
        "collaborators": collaborators,
        "time_diffs": time_diffs
    }


def get_dev_commits(repository_owner, repository_name, access_token):
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