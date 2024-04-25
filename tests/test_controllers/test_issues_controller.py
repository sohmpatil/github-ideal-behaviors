import tests.test_controllers.mock_requests as mock_requests

from controllers.issues_controller import get_issues
from models.issues_model import IssueList, Issue, User, Assignee


def test_get_issues_success():
    """
    Test the get_issues() method to ensure it successfully retrieves a list of issues.

    This test case mocks a successful response from the GitHub API and checks if the method correctly
    parses the response and returns an IssueList object with the expected issues. It verifies the
    length of the issues list and the details of each issue to ensure they match the expected values.

    Returns:
        None
    """
    expected = IssueList(issues=[
        Issue(
            id=2203316067,
            user=User(login="sanket8397"),
            assignee=Assignee(login="sanket8397"),
            assignees=[
                Assignee(login="sanket8397"),
                Assignee(login="sanikag123"),
            ],
            closed_at=None,
            created_at="2024-03-22T20:57:28Z",
            updated_at="2024-03-22T20:57:28Z"
        ),
        Issue(
            id=124,
            user=User(login="test"),
            assignee=None,
            assignees=[],
            closed_at=None,
            created_at="2024-03-21T11:45:00Z",
            updated_at="2024-03-23T09:20:00Z"
        )
    ])

    # * Setup mock request and response
    mock_requests.mock_response_func = lambda: mock_requests.MockResponse(
        status_code=200,
        response_key="MockIssuesResponse"
    )
    got = get_issues(
        repo_owner="test_owner",
        repo_name="test_name",
        access_token="test_token",
        requests=mock_requests
    )

    assert len(got.issues)

    assert got.issues[0].id == expected.issues[0].id
    assert got.issues[0].user.login == expected.issues[0].user.login
    assert got.issues[0].assignee.login == expected.issues[0].assignee.login
    assert got.issues[0].assignees[0].login == expected.issues[0].assignees[0].login
    assert got.issues[0].assignees[1].login == expected.issues[0].assignees[1].login
    assert got.issues[0].closed_at == expected.issues[0].closed_at
    assert got.issues[0].created_at == expected.issues[0].created_at
    assert got.issues[0].updated_at == expected.issues[0].updated_at

    assert got.issues[1].id == expected.issues[1].id
    assert got.issues[1].user.login == expected.issues[1].user.login
    assert not got.issues[1].assignee
    assert not got.issues[1].assignees
    assert got.issues[1].closed_at == expected.issues[1].closed_at
    assert got.issues[1].created_at == expected.issues[1].created_at
    assert got.issues[1].updated_at == expected.issues[1].updated_at


def test_get_issues_empty():
    """
    Test the get_issues() method to ensure it handles an empty response correctly.

    This test case mocks a response with a 401 status code, simulating an unauthorized request. It checks
    if the method correctly handles this case and returns an empty IssueList object.

    Returns:
        None
    """
    mock_requests.mock_response_func = lambda: mock_requests.MockResponse(
        status_code=401,
        response_key="MockIssuesResponse"
    )
    got = get_issues(
        repo_owner="test_owner",
        repo_name="test_name",
        access_token="test_token",
        requests=mock_requests
    )

    assert not len(got.issues)
