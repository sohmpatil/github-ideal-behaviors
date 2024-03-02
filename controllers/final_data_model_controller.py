import logging

from models.final_model import CollaboratorCommit, CollaboratorCommitList
from models.bad_boys import RepositoryAnalysisInput
from controllers.commit_details_controller import get_commit_details
from controllers.commits_controller import get_commits
from controllers.collaborators_controller import get_collaborators\

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("final_data_controller")


def final_data_controller(request: RepositoryAnalysisInput) -> CollaboratorCommitList:
    final_data = []

    collaborators = get_collaborators(
        request.repository_owner,
        request.repository_name,
        request.git_access_token
    )

    log.info(collaborators)
    for collaborator in collaborators.collaborators:
        commits_details = []
        commits = get_commits(
            request.repository_owner,
            request.repository_name,
            request.git_access_token,
            collaborator.login
        )
        for commit in commits.commits:
            commit_detail = get_commit_details(
                request.repository_owner,
                request.repository_name,
                commit.sha,
                request.git_access_token
            )
            commits_details.append(commit_detail)

        collaborator_commit = CollaboratorCommit(
            collaborator=collaborator, 
            commits=commits_details
        )
        final_data.append(collaborator_commit)

    final_data_model = CollaboratorCommitList(data=final_data)
    return final_data_model
