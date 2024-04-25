import logging
import requests

from models.collaborator_commit_model import CollaboratorCommit, CollaboratorCommitList, IndividualCollaboratorCommit
from models.repository_io_model import RepositoryAnalysisInput, RepositoryAnalysisIndividualInput
from controllers.commit_details_controller import get_commit_details
from controllers.commits_controller import get_commits
from controllers.issues_controller import get_issues
from controllers.collaborators_controller import get_collaborators
from controllers.pull_requests_controller import get_pull_requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("collaborator_data_model_controller")


def collaborator_data_controller(request: RepositoryAnalysisInput, requests=requests) -> CollaboratorCommitList:
    """
    Analyze repository data to gather information about collaborators, commits, pull requests, and issues and save it in CollaboratorCommitList model.

    Args:
        request (RepositoryAnalysisInput): An input object containing repository name, owner and access token.

    Returns:
        CollaboratorCommitList: A list containing detailed information about each collaborator's commits, 
            created and assigned pull requests, and created and assigned issues.

    Raises:
        None.

    Note:
        This function utilizes several helper functions (`get_collaborators`, `get_pull_requests`, 
        `get_issues`, `get_commits`, and `get_commit_details`) to retrieve repository data.

        CollaboratorCommitList and related models must be imported from appropriate modules.
    """
    final_data = []

    collaborators = get_collaborators(
        request.repository_owner,
        request.repository_name,
        request.git_access_token,
        requests=requests
    )
    pull_requests = get_pull_requests(
        request.repository_owner,
        request.repository_name,
        request.git_access_token,
        requests=requests
    )
    issues = get_issues(
        request.repository_owner,
        request.repository_name,
        request.git_access_token,
        requests=requests
    )

    for collaborator in collaborators.collaborators:
        commits_details = []
        commits = get_commits(
            request.repository_owner,
            request.repository_name,
            request.git_access_token,
            collaborator.login,
            requests=requests
        )
        log.info(f'{collaborator.login}: {len(commits.commits) if commits else 0} commits.')

        for commit in commits.commits:
            commit_detail = get_commit_details(
                request.repository_owner,
                request.repository_name,
                commit.sha,
                request.git_access_token,
                requests=requests
            )
            if commit_detail:
                commits_details.append(commit_detail)
                
        pr_created = []
        pr_assigned = []

        for pull_request in pull_requests.pull_requests:
            if pull_request.creator == collaborator.login:
                pr_created.append(pull_request)
            elif collaborator.login in pull_request.pr_assignees:
                pr_assigned.append(pull_request)

        issue_assigned = []
        issue_created = []

        for issue in issues.issues:
            if issue.assignee.login == collaborator.login:
                issue_assigned.append(issue)
            if issue.user.login == collaborator.login:
                issue_created.append(issue)

        collaborator_commit = CollaboratorCommit(
            collaborator=collaborator, 
            commits=commits_details,
            pr_created=pr_created,
            pr_assigned=pr_assigned,
            issue_created=issue_created,
            issue_assigned=issue_assigned
        )
        final_data.append(collaborator_commit)
 
    final_data_model = CollaboratorCommitList(data=final_data)
    return final_data_model


def collaborator_individual_data_controller(request: RepositoryAnalysisIndividualInput, requests=requests) -> IndividualCollaboratorCommit:
    """
    Analyze individual collaborator data to gather information about their commits, 
    created and assigned pull requests, and created and assigned issues.

    Args:
        request (RepositoryAnalysisIndividualInput): An input object containing repository owner, repository name,
            collaborator's username, and access token.

    Returns:
        IndividualCollaboratorCommit: Detailed information about the collaborator's commits, 
            created and assigned pull requests, and created and assigned issues.

    Raises:
        None.

    Note:
        This function utilizes helper functions (`get_commits`, `get_commit_details`, `get_pull_requests`, 
        and `get_issues`) to retrieve repository data.

        IndividualCollaboratorCommit model must be imported from the appropriate module.
    """
    commits_details = []
    commits = get_commits(
        request.repository_owner,
        request.repository_name,
        request.git_access_token,
        request.collaborator_username,
        requests=requests
    )
    log.info(f'{request.collaborator_username}: {len(commits.commits) if commits else 0} commits.')

    for commit in commits.commits:
        commit_detail = get_commit_details(
            request.repository_owner,
            request.repository_name,
            commit.sha,
            request.git_access_token,
            requests=requests
        )
        if commit_detail:
            commits_details.append(commit_detail)

    pr_created = []
    pr_assigned = []
    pull_requests = get_pull_requests(
        request.repository_owner,
        request.repository_name,
        request.git_access_token,
        requests=requests
    )
    for pull_request in pull_requests.pull_requests:
        if pull_request.creator == request.collaborator_username:
            pr_created.append(pull_request)
        elif request.collaborator_username in pull_request.pr_assignees:
            pr_assigned.append(pull_request)

    issues = get_issues(
        request.repository_owner,
        request.repository_name,
        request.git_access_token,
        requests=requests
    )
    issue_assigned = []
    issue_created = []
    for issue in issues.issues:
        if issue.assignee.login == request.collaborator_username:
            issue_assigned.append(issue)
        if issue.user.login == request.collaborator_username:
            issue_created.append(issue)

    collaborator_commit = IndividualCollaboratorCommit(
        commits=commits_details,
        pr_created=pr_created,
        pr_assigned=pr_assigned,
        issue_created=issue_created,
        issue_assigned=issue_assigned
    )
    return collaborator_commit
