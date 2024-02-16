from fastapi import FastAPI
import logging
import utils.github_utils as git_utils
import utils.rules_util as rules_utils
from models.data_model import RepositoryAnalysisInput 

app = FastAPI()


# Set up logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

RULES_FOLDER_PATH = './rules'
RULES_FILE = 'Group10Rules.jsonc'

@app.post("/gitbehaviors")
def analyze_repository(data: RepositoryAnalysisInput):

    dev_commits = get_dev_commits(data.repository_owner, data.repository_name, data.git_access_token)
    log.info(dev_commits)

<<<<<<< HEAD
    commits = git_utils.get_commits(
        repository_owner,  
        repository_name,  
        git_access_token
    )

    log.info(commits)
    log.info(len(commits))
=======
    commits = git_utils.get_commits(data.repository_owner, data.repository_name, data.git_access_token)
    log.info(commits)
    
>>>>>>> 1392283 (minor refactoring and update README)
    if commits:
        log. info(f"Commits List of {data.repository_owner}/{data.repository_name}:")
        for commit in commits:
            files_extension_dict = git_utils.get_changed_files(
                data.repository_owner,
                data.repository_name,
                commit,
                data.git_access_token
            )
            log.info(f"Commit ID: {commit}")
            log.info(f"Extension Counts {dict(files_extension_dict)}")
            log.info(f"Total changed files in the commit: \
                     {sum(files_extension_dict.values())}")
    else:
        log.info("No commits found.")

    if commits:
        log.info(f"Commits List of {data.repository_owner}/{data.repository_name}:")
        for commit in commits:
            git_utils.get_number_of_new_lines(
                data.repository_owner,
                data.repository_name,
                commit,
                data.git_access_token
            )

            git_utils.get_number_of_changes_by_author(
                repository_owner,
                repository_name,
                commit,
                git_access_token)

    else:
        log.info("No commits found.")

    collaborators = git_utils.get_collaborators(
        data.repository_owner, data.repository_name, data.git_access_token)
    for collaborator in collaborators:
        log.info(f"Time difference in consecutive commits for {collaborator}")
        time_diffs = git_utils.fetch_consecutive_time_between_commits(
            data.repository_owner,  
            data.repository_name,  
            data.git_access_token,  
            collaborator
        )
        log.info(time_diffs)



    rules = rules_utils.load_rules(RULES_FOLDER_PATH, RULES_FILE)

    # You can use RULE global variable from rules_util as well
    print(rules, rules_utils.RULES)
    print("meaningfulLinesThreshold", rules['meaningfulLinesThreshold'])
    print("minCommits", rules['minCommits'])
    print("minLines", rules['minLines'])
    print("minBlame", rules['minBlame'])
    print("minTimeBetweenCommits", rules['minTimeBetweenCommits'])
    print("maxFilesPerCommit", rules['maxFilesPerCommit'])
    print("allowedFileTypes", rules['allowedFileTypes'])

    # Return the results
    return {
        "dev_commits": dev_commits,
        "commits": commits,
      #  "collaborators": collaborators,
      #  "time_diffs": time_diffs
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
