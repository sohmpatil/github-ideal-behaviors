import json
from models import issues_model

def test_issue():
    """
    Tests the creation and properties of an IssueList object.

    This function creates an IssueList object with sample data and asserts
    that the object's properties match the expected values. It checks the number of
    issues in the list, the details of each issue, including the issue ID, user login,
    assignee login, assignees list, and timestamps for creation and update.
    """
    json_str = r"""
    {
        "issues": [
            {
                "id": 2203316067,
                "user": {
                    "login": "sanket8397"
                },
                "assignee": {
                    "login": "sanket8397"
                },
                "assignees": [
                    {
                        "login": "sanket8397"
                    },
                    {
                        "login": "sanikag123"
                    }
                ],
                "closed_at": null,
                "created_at": "2024-03-22T20:57:28Z",
                "updated_at": "2024-03-22T20:57:28Z"
            },
            {
                "id": 124,
                "user": {
                    "login": "test"
                },
                "assignee": null,
                "assignees": [],
                "closed_at": null,
                "created_at": "2024-03-21T11:45:00Z",
                "updated_at": "2024-03-23T09:20:00Z"
            }
        ]
    }
    """
    to_dict = json.loads(json_str)
    got = issues_model.IssueList(**to_dict)
    
    assert isinstance(got, issues_model.IssueList)
    assert len(got.issues) == 2
    assert got.issues[0].id == 2203316067
    assert got.issues[0].user.login == "sanket8397"
    assert got.issues[0].assignee.login == "sanket8397"
    assert got.issues[0].assignees[0].login == "sanket8397"
    assert got.issues[0].assignees[1].login == "sanikag123"
    assert got.issues[0].closed_at is None
    assert got.issues[0].created_at == "2024-03-22T20:57:28Z"
    assert got.issues[0].updated_at == "2024-03-22T20:57:28Z"
    assert got.issues[1].id == 124
    assert got.issues[1].user.login == "test"
    assert got.issues[1].assignee is None
    assert got.issues[1].assignees == []
    assert got.issues[1].closed_at is None
    assert got.issues[1].created_at == "2024-03-21T11:45:00Z"
    assert got.issues[1].updated_at == "2024-03-23T09:20:00Z"
