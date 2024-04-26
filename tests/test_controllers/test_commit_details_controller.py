import tests.test_controllers.mock_requests as mock_requests

from controllers.commit_details_controller import get_commit_details
from models.commit_details_model import CommitDetail


def test_get_commits_success():
    """Test get_commits() method for a successful response."""
    expected = CommitDetail(sha="6dcb09b5b57875f334f61aebed695e2e4193db5e")

    # * Setup mock request and response
    mock_requests.mock_response_func = lambda: mock_requests.MockResponse(
        status_code=200,
        response_key="MockCommitDetailsResponse"
    )
    got = get_commit_details(
        owner="test_owner",
        repo="test_name",
        commit_sha="6dcb09b5b57875f334f61aebed695e2e4193db5e",
        access_token="test_token",
        requests=mock_requests
    )

    assert got.sha == expected.sha


def test_get_commits_empty():
    """Test get_commits() method for an invalid status_code."""
    # * Setup mock request and response
    mock_requests.mock_response_func = lambda: mock_requests.MockResponse(
        status_code=401,
        response_key="MockCommitDetailsResponse"
    )
    got = get_commit_details(
        owner="test_owner",
        repo="test_name",
        commit_sha="some_sha1",
        access_token="test_token",
        requests=mock_requests
    )

    assert got is None
