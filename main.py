from fastapi import FastAPI
from collections import defaultdict
import logging
import utils.github_utils as git_utils
import json5
from models.data_model import RepositoryAnalysisInput, ValidationRules
from utils.rules_util import load_rules

app = FastAPI()


# Set up logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

RULES_FOLDER_PATH = './rules'
RULES_FILE = 'Group10Rules.jsonc'
RULES: ValidationRules = None


@app.on_event("startup")
async def startup_event():
    global RULES
    RULES = load_rules(RULES_FOLDER_PATH, RULES_FILE)


@app.post("/gitbehaviors")
def analyze_repository(data: RepositoryAnalysisInput):

    dev_commits = get_dev_commits(
        data.repository_owner, 
        data.repository_name, 
        data.git_access_token
    )
    log.info(dev_commits)

    commits = git_utils.get_commits(
        data.repository_owner, 
        data.repository_name, 
        data.git_access_token
    )
    log.info(commits)

    rules = RULES
    # You can use RULE global variable from rules_util as well
    log.info(f'rules: {rules}')

    violations = defaultdict(list)
    # 1. check violation for min commits rule per developer
    for dev, count in dev_commits.items():
        if count < rules.minCommits:
            violations['minCommits'].append(dev)

    if commits:
        log.info(
            f"Commits List of {data.repository_owner}/{data.repository_name}:")
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
            # 2. check violation of allowed file types rule per commit
            allowed_file_types = set(rules.allowedFileTypes)
            for ext in files_extension_dict:
                if ext not in allowed_file_types:
                    violations['allowedFileTypes'].append(commit)
            # 7. check violation of max number of allowed files per commit
            if sum(files_extension_dict.values()) > rules.maxFilesPerCommit:
                violations['maxFilesPerCommit'].append(commit)
            
            additions, deletions = git_utils.get_number_of_new_lines(
                data.repository_owner,
                data.repository_name,
                commit,
                data.git_access_token
            )
            # 3. check violation for min lines added overall
            if additions - deletions < rules.minLines:
                violations['minLines'].append(commit)
            # 4. check violation for min blame per commit
            if additions < rules.minBlame:
                violations['minBlame'].append(commit)

            meaningful_lines = git_utils.get_meaningful_lines(
                data.repository_owner,
                data.repository_name,
                commit,
                data.git_access_token
            )
            # 5. check violation for meaningful lines per commit
            if meaningful_lines < rules.meaningfulLinesThreshold:
                violations['meaningfulLinesThreshold'].append(commit)
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
        if not all(map(lambda diff: diff >= rules.minTimeBetweenCommits, time_diffs)):
            violations['minTimeBetweenCommits'].append(collaborator)

    # Return the results
    log.info(violations)
    return json5.dumps(violations)

@app.get("/test")
def test():
    log.info(RULES)


def get_dev_commits(repository_owner, repository_name, access_token):
    """Gt number of commits for each developer"""
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
