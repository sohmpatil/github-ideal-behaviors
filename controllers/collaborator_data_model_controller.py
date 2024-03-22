import logging

from models.collaborator_commit_model import CollaboratorCommit, CollaboratorCommitList, IndividualCollaboratorCommit
from models.repository_io_model import RepositoryAnalysisInput, RepositoryAnalysisIndividualInput
from controllers.commit_details_controller import get_commit_details
from controllers.commits_controller import get_commits
from controllers.collaborators_controller import get_collaborators
from controllers.pull_requests_controller import get_pull_requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("collaborator_data_model_controller")


def collaborator_data_controller(request: RepositoryAnalysisInput) -> CollaboratorCommitList:
    final_data = []

    collaborators = get_collaborators(
        request.repository_owner,
        request.repository_name,
        request.git_access_token
    )
    pull_requests = get_pull_requests(
        request.repository_owner,
        request.repository_name,
        request.git_access_token
    )

    for collaborator in collaborators.collaborators:
        commits_details = []
        commits = get_commits(
            request.repository_owner,
            request.repository_name,
            request.git_access_token,
            collaborator.login
        )
        log.info(f'{collaborator.login}: {len(commits.commits) if commits else 0} commits.')

        for commit in commits.commits:
            commit_detail = get_commit_details(
                request.repository_owner,
                request.repository_name,
                commit.sha,
                request.git_access_token
            )
            commits_details.append(commit_detail)
        pr_created = []
        pr_assigned = []

        for pull_request in pull_requests.pull_requests:
            if pull_request.creator == collaborator.login:
                pr_created.append(pull_request)
            elif collaborator.login in pull_request.pr_assignees:
                pr_assigned.append(pull_request)

        collaborator_commit = CollaboratorCommit(
            collaborator=collaborator, 
            commits=commits_details,
            pr_created=pr_created,
            pr_assigned=pr_assigned
        )
        final_data.append(collaborator_commit)
 
    final_data_model = CollaboratorCommitList(data=final_data)
    return final_data_model



def collaborator_individual_data_controller(request: RepositoryAnalysisIndividualInput) -> IndividualCollaboratorCommit:
    commits_details = []
    commits = get_commits(
        request.repository_owner,
        request.repository_name,
        request.git_access_token,
        request.collaborator_username
    )
    log.info(f'{request.collaborator_username}: {len(commits.commits) if commits else 0} commits.')

    for commit in commits.commits:
        commit_detail = get_commit_details(
            request.repository_owner,
            request.repository_name,
            commit.sha,
            request.git_access_token
        )
        commits_details.append(commit_detail)
    pr_created = []
    pr_assigned = []

    pull_requests = get_pull_requests(
        request.repository_owner,
        request.repository_name,
        request.git_access_token
    )

    for pull_request in pull_requests.pull_requests:
        if pull_request.creator == request.collaborator_username:
            pr_created.append(pull_request)
        elif request.collaborator_username in pull_request.pr_assignees:
            pr_assigned.append(pull_request)

    collaborator_commit = IndividualCollaboratorCommit(
        commits=commits_details,
        pr_created=pr_created,
        pr_assigned=pr_assigned
    )
    return collaborator_commit
