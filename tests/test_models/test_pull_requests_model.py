import json
from models import pull_requests_model

def test_pull_requests():
    """
    Tests the creation and properties of a PullRequests object.

    This function creates a PullRequests object with sample data and asserts
    that the object's properties match the expected values. It checks the pull request's
    creator, ID, assignees, creation and closure timestamps, state, and merge commit SHA.
    """
    pull_requests_json_str = """
    {
        "creator": "rhish9h",
        "id": 1143972904,
        "pr_assignees": ["test1", "test2"],
        "created_at": "2022-12-03T03:33:04Z",
        "closed_at": "2022-12-03T03:33:55Z",
        "state": "closed",
        "merge_commit_sha": "e89f7a33d84b4057b8cfe9074a8b38f45bcb7804"
    }
    """

    pull_requests_data = json.loads(pull_requests_json_str)

    pull_requests_obj = pull_requests_model.PullRequests(**pull_requests_data)

    assert pull_requests_obj.creator == "rhish9h"
    assert pull_requests_obj.id == 1143972904
    assert len(pull_requests_obj.pr_assignees) == 2
    assert pull_requests_obj.pr_assignees == ["test1", "test2"]
    assert pull_requests_obj.created_at == "2022-12-03T03:33:04Z"
    assert pull_requests_obj.closed_at == "2022-12-03T03:33:55Z"
    assert pull_requests_obj.state == "closed"
    assert pull_requests_obj.merge_commit_sha == "e89f7a33d84b4057b8cfe9074a8b38f45bcb7804"

def test_pull_requests_list():
    """
    Tests the creation and properties of a PullRequestsList object.

    This function creates a PullRequestsList object with sample data and asserts
    that the object's properties match the expected values. It checks the number of
    pull requests in the list and the details of each pull request, including the
    creator, ID, assignees, creation and closure timestamps, state, and merge commit SHA.
    """
    pull_requests_list_json_str = """
    {
        "pull_requests": [
            {
                "creator": "rhish9h",
                "id": 1143972904,
                "pr_assignees": ["test1", "test2"],
                "created_at": "2022-12-03T03:33:04Z",
                "closed_at": "2022-12-03T03:33:55Z",
                "state": "closed",
                "merge_commit_sha": "e89f7a33d84b4057b8cfe9074a8b38f45bcb7804"
            },
            {
                "creator": "sanket8397",
                "id": 1143944226,
                "pr_assignees": ["test1"],
                "created_at": "2024-03-26T11:20:00Z",
                "closed_at": null,
                "state": "open",
                "merge_commit_sha": null
            }
        ]
    }
    """

   
    pull_requests_list_data = json.loads(pull_requests_list_json_str)

    pull_requests_list_obj = pull_requests_model.PullRequestsList(**pull_requests_list_data)

    assert len(pull_requests_list_obj.pull_requests) == 2
    assert pull_requests_list_obj.pull_requests[0].creator == "rhish9h"
    assert pull_requests_list_obj.pull_requests[0].id == 1143972904
    assert len(pull_requests_list_obj.pull_requests[0].pr_assignees) == 2
    assert pull_requests_list_obj.pull_requests[0].pr_assignees == ["test1", "test2"]
    assert pull_requests_list_obj.pull_requests[0].created_at == "2022-12-03T03:33:04Z"
    assert pull_requests_list_obj.pull_requests[0].closed_at == "2022-12-03T03:33:55Z"
    assert pull_requests_list_obj.pull_requests[0].state == "closed"
    assert pull_requests_list_obj.pull_requests[0].merge_commit_sha == "e89f7a33d84b4057b8cfe9074a8b38f45bcb7804"
    assert pull_requests_list_obj.pull_requests[1].creator == "sanket8397"
    assert pull_requests_list_obj.pull_requests[1].id == 1143944226
    assert len(pull_requests_list_obj.pull_requests[1].pr_assignees) == 1
    assert pull_requests_list_obj.pull_requests[1].pr_assignees == ["test1"]
    assert pull_requests_list_obj.pull_requests[1].created_at == "2024-03-26T11:20:00Z"
    assert pull_requests_list_obj.pull_requests[1].closed_at is None
    assert pull_requests_list_obj.pull_requests[1].state == "open"
    assert pull_requests_list_obj.pull_requests[1].merge_commit_sha is None
