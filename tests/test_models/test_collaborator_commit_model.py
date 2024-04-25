import json
from models import collaborator_commit_model

def test_collaborator_commit():
    """
    Tests the creation and properties of a CollaboratorCommit object.

    This function creates a CollaboratorCommit object with sample data and asserts
    that the object's properties match the expected values. It checks the collaborator's
    login, the number and details of commits, pull requests created and assigned,
    and issues created and assigned.
    """
    data = {
        "collaborator": {"login": "sanikag123"},
        "commits": [{"sha": "e89f7a33d84b4057b8cfe9074a8b38f45bcb7804"}],
        "pr_created": [{"id": 123, "created_at": "2022-01-01T00:00:00Z", "state": "open"}],
        "pr_assigned": [{"id": 456, "created_at": "2022-01-02T00:00:00Z", "state": "closed"}],
        "issue_created": [{"id": 789, "user": {"login": "sanket8397"}, "assignees": [{"login": "sohmpatil"}]}],
        "issue_assigned": [{"id": 101112, "user": {"login": "sanket8397"}, "assignees": [{"login": "sohmpatil"}]}]
    }

    collaborator_commit = collaborator_commit_model.CollaboratorCommit(**data)

    assert collaborator_commit.collaborator.login == "sanikag123"
    assert len(collaborator_commit.commits) == 1
    assert collaborator_commit.commits[0].sha == "e89f7a33d84b4057b8cfe9074a8b38f45bcb7804"
    assert len(collaborator_commit.pr_created) == 1
    assert collaborator_commit.pr_created[0].id == 123
    assert collaborator_commit.pr_created[0].created_at == "2022-01-01T00:00:00Z"
    assert collaborator_commit.pr_created[0].state == "open"
    assert len(collaborator_commit.pr_assigned) == 1
    assert collaborator_commit.pr_assigned[0].id == 456
    assert collaborator_commit.pr_assigned[0].created_at == "2022-01-02T00:00:00Z"
    assert collaborator_commit.pr_assigned[0].state == "closed"
    assert len(collaborator_commit.issue_created) == 1
    assert collaborator_commit.issue_created[0].id == 789
    assert collaborator_commit.issue_created[0].user.login == "sanket8397"
    assert collaborator_commit.issue_created[0].assignees[0].login == "sohmpatil"
    assert len(collaborator_commit.issue_assigned) == 1
    assert collaborator_commit.issue_assigned[0].id == 101112
    assert collaborator_commit.issue_assigned[0].user.login == "sanket8397"
    assert collaborator_commit.issue_assigned[0].assignees[0].login == "sohmpatil"

def test_individual_collaborator_commit():
    """
    Tests the creation and properties of an IndividualCollaboratorCommit object.

    This function creates an IndividualCollaboratorCommit object with sample data and asserts
    that the object's properties match the expected values. It checks the number and details of
    commits, pull requests created and assigned, and issues created and assigned.
    """
    data = {
        "commits": [{"sha": "abcdef"}],
        "pr_created": [{"id": 123, "created_at": "2022-01-01T00:00:00Z", "state": "open"}],
        "pr_assigned": [{"id": 456, "created_at": "2022-01-02T00:00:00Z", "state": "closed"}],
        "issue_created": [{"id": 789, "user": {"login": "sanikag123"}, "assignees": [{"login": "sanket8397"}]}],
        "issue_assigned": [{"id": 101112, "user": {"login": "sohmpatil"}, "assignees": [{"login": "sohmpatil"}]}]
    }

    individual_collaborator_commit = collaborator_commit_model.IndividualCollaboratorCommit(**data)

    assert len(individual_collaborator_commit.commits) == 1
    assert individual_collaborator_commit.commits[0].sha == "abcdef"
    assert len(individual_collaborator_commit.pr_created) == 1
    assert individual_collaborator_commit.pr_created[0].id == 123
    assert individual_collaborator_commit.pr_created[0].created_at == "2022-01-01T00:00:00Z"
    assert individual_collaborator_commit.pr_created[0].state == "open"
    assert len(individual_collaborator_commit.pr_assigned) == 1
    assert individual_collaborator_commit.pr_assigned[0].id == 456
    assert individual_collaborator_commit.pr_assigned[0].created_at == "2022-01-02T00:00:00Z"
    assert individual_collaborator_commit.pr_assigned[0].state == "closed"
    assert len(individual_collaborator_commit.issue_created) == 1
    assert individual_collaborator_commit.issue_created[0].id == 789
    assert individual_collaborator_commit.issue_created[0].user.login == "sanikag123"
    assert individual_collaborator_commit.issue_created[0].assignees[0].login == "sanket8397"
    assert len(individual_collaborator_commit.issue_assigned) == 1
    assert individual_collaborator_commit.issue_assigned[0].id == 101112
    assert individual_collaborator_commit.issue_assigned[0].user.login == "sohmpatil"
    assert individual_collaborator_commit.issue_assigned[0].assignees[0].login == "sohmpatil"

def test_collaborator_commit_list():
    """
    Tests the creation and properties of a CollaboratorCommitList object.

    This function creates a CollaboratorCommitList object with sample data and asserts
    that the object's properties match the expected values. It checks the number of items in
    the list and the properties of each CollaboratorCommit object within the list.
    """
    data = {
        "data": [
            {
                "collaborator": {"login": "sanikag123"},
                "commits": [{"sha": "abcdef"}],
                "pr_created": [{"id": 123, "created_at": "2022-01-01T00:00:00Z", "state": "open"}],
                "pr_assigned": [{"id": 456, "created_at": "2022-01-02T00:00:00Z", "state": "closed"}],
                "issue_created": [{"id": 789, "user": {"login": "sanket8397"}, "assignees": [{"login": "hsakhuja"}]}],
                "issue_assigned": [{"id": 101112, "user": {"login": "sohmpatil"}, "assignees": [{"login": "hsakhuja"}]}]
            },
            {
                "collaborator": {"login": "sanket8397"},
                "commits": [{"sha": "ghijkl"}],
                "pr_created": [{"id": 124, "created_at": "2022-01-03T00:00:00Z", "state": "open"}],
                "pr_assigned": [{"id": 457, "created_at": "2022-01-04T00:00:00Z", "state": "closed"}],
                "issue_created": [{"id": 790, "user": {"login": "hsakhuja"}, "assignees": [{"login": "sohmpatil"}]}],
                "issue_assigned": [{"id": 101113, "user": {"login": "sohmpatil"}, "assignees": [{"login": "hsakhuja"}]}]
            }
        ]
    }

    collaborator_commit_list = collaborator_commit_model.CollaboratorCommitList(**data)

    assert len(collaborator_commit_list.data) == 2

    assert collaborator_commit_list.data[0].collaborator.login == "sanikag123"
    assert len(collaborator_commit_list.data[0].commits) == 1
    assert collaborator_commit_list.data[0].commits[0].sha == "abcdef"
    assert len(collaborator_commit_list.data[0].pr_created) == 1
    assert collaborator_commit_list.data[0].pr_created[0].id == 123
    assert collaborator_commit_list.data[0].pr_created[0].created_at == "2022-01-01T00:00:00Z"
    assert collaborator_commit_list.data[0].pr_created[0].state == "open"
    assert len(collaborator_commit_list.data[0].pr_assigned) == 1
    assert collaborator_commit_list.data[0].pr_assigned[0].id == 456
    assert collaborator_commit_list.data[0].pr_assigned[0].created_at == "2022-01-02T00:00:00Z"
    assert collaborator_commit_list.data[0].pr_assigned[0].state == "closed"
    assert len(collaborator_commit_list.data[0].issue_created) == 1
    assert collaborator_commit_list.data[0].issue_created[0].id == 789
    assert collaborator_commit_list.data[0].issue_created[0].user.login == "sanket8397"
    assert collaborator_commit_list.data[0].issue_created[0].assignees[0].login == "hsakhuja"
    assert len(collaborator_commit_list.data[0].issue_assigned) == 1
    assert collaborator_commit_list.data[0].issue_assigned[0].id == 101112
    assert collaborator_commit_list.data[0].issue_assigned[0].user.login == "sohmpatil"
    assert collaborator_commit_list.data[0].issue_assigned[0].assignees[0].login == "hsakhuja"

    assert collaborator_commit_list.data[1].collaborator.login == "sanket8397"
    assert len(collaborator_commit_list.data[1].commits) == 1
    assert collaborator_commit_list.data[1].commits[0].sha == "ghijkl"
    assert len(collaborator_commit_list.data[1].pr_created) == 1
    assert collaborator_commit_list.data[1].pr_created[0].id == 124
    assert collaborator_commit_list.data[1].pr_created[0].created_at == "2022-01-03T00:00:00Z"
    assert collaborator_commit_list.data[1].pr_created[0].state == "open"
    assert len(collaborator_commit_list.data[1].pr_assigned) == 1
    assert collaborator_commit_list.data[1].pr_assigned[0].id == 457
    assert collaborator_commit_list.data[1].pr_assigned[0].created_at == "2022-01-04T00:00:00Z"
    assert collaborator_commit_list.data[1].pr_assigned[0].state == "closed"
    assert len(collaborator_commit_list.data[1].issue_created) == 1
    assert collaborator_commit_list.data[1].issue_created[0].id == 790
    assert collaborator_commit_list.data[1].issue_created[0].user.login == "hsakhuja"
    assert collaborator_commit_list.data[1].issue_created[0].assignees[0].login == "sohmpatil"
    assert len(collaborator_commit_list.data[1].issue_assigned) == 1
    assert collaborator_commit_list.data[1].issue_assigned[0].id == 101113
    assert collaborator_commit_list.data[1].issue_assigned[0].user.login == "sohmpatil"
    assert collaborator_commit_list.data[1].issue_assigned[0].assignees[0].login == "hsakhuja"
