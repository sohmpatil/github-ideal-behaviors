import tests.test_controllers.mock_requests as mock_requests

from controllers.pull_requests_controller import get_pull_requests
from models.pull_requests_model import PullRequestsList, PullRequests


def test_get_pull_requests_success():
    """
    Test the get_pull_requests() method to ensure it successfully retrieves a list of pull requests.

    This test case mocks a successful response from the GitHub API and checks if the method correctly
    parses the response and returns a PullRequestsList object with the expected pull requests. It verifies the
    length of the pull requests list and the details of each pull request to ensure they match the expected values.

    Returns:
        None
    """
    expected = PullRequestsList(pull_requests=[
        PullRequests(
            creator="rhish9h",
            id=1143972904,
            pr_assignees=["test1", "test2"],
            created_at="2022-12-03T03:33:04Z",
            closed_at="2022-12-03T03:33:55Z",
            state="closed",
            merge_commit_sha="e89f7a33d84b4057b8cfe9074a8b38f45bcb7804"
        ),
        PullRequests(
            creator="sanket8397",
            id=1143944226,
            pr_assignees=["test1"],
            created_at="2024-03-26T11:20:00Z",
            closed_at=None,
            state="open",
            merge_commit_sha=None
        )
    ])

    # * Setup mock request and response
    mock_requests.mock_response_func = lambda: mock_requests.MockResponse(
        status_code=200,
        response_key="MockPullRequestsResponse"
    )
    got = get_pull_requests(
        repo_owner="test_owner",
        repo_name="test_name",
        access_token="test_token",
        requests=mock_requests
    )

    assert len(got.pull_requests)

    assert got.pull_requests[0].creator == expected.pull_requests[0].creator
    assert got.pull_requests[0].id == expected.pull_requests[0].id
    assert got.pull_requests[0].pr_assignees == expected.pull_requests[0].pr_assignees
    assert got.pull_requests[0].created_at == expected.pull_requests[0].created_at
    assert got.pull_requests[0].closed_at == expected.pull_requests[0].closed_at
    assert got.pull_requests[0].state == expected.pull_requests[0].state
    assert got.pull_requests[0].merge_commit_sha == expected.pull_requests[0].merge_commit_sha

    assert got.pull_requests[1].creator == expected.pull_requests[1].creator
    assert got.pull_requests[1].id == expected.pull_requests[1].id
    assert got.pull_requests[1].pr_assignees == expected.pull_requests[1].pr_assignees
    assert got.pull_requests[1].created_at == expected.pull_requests[1].created_at
    assert got.pull_requests[1].closed_at == expected.pull_requests[1].closed_at
    assert got.pull_requests[1].state == expected.pull_requests[1].state
    assert got.pull_requests[1].merge_commit_sha == expected.pull_requests[1].merge_commit_sha


def test_get_pull_requests_empty():
    """
    Test the get_pull_requests() method to ensure it handles an empty response correctly.

    This test case mocks a response with a 401 status code, simulating an unauthorized request. It checks
    if the method correctly handles this case and returns an empty PullRequestsList object.

    Returns:
        None
    """
    mock_requests.mock_response_func = lambda: mock_requests.MockResponse(
        status_code=401,
        response_key="MockPullRequestsResponse"
    )
    got = get_pull_requests(
        repo_owner="test_owner",
        repo_name="test_name",
        access_token="test_token",
        requests=mock_requests
    )

    assert not len(got.pull_requests)
