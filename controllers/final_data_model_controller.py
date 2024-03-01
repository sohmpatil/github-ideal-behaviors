from models.final_model import CollaboratorCommit, CollaboratorCommitList
from controllers.commit_details_controller import get_commit_details
from controllers.commits_controller import get_commits
from controllers.collaborators_controller import get_collaborators

def final_data_controller(repo_owner, repo_name, access_token):
    final_data = []

    collaborators = get_collaborators(repo_owner, repo_name, access_token)
    print(collaborators)
    for collaborator in collaborators.collaborators:
        commits_details = []
        commits = get_commits(repo_owner, repo_name,
                            access_token, collaborator.login)
        for commit in commits.commits:
            commit_detail = get_commit_details(
                repo_owner, repo_name, commit.sha, access_token)
            commits_details.append(commit_detail)

        collaborator_commit = CollaboratorCommit(
            collaborator=collaborator, commits=commits_details)
        final_data.append(collaborator_commit)


    final_data_model = CollaboratorCommitList(data=final_data)
    return final_data_model
