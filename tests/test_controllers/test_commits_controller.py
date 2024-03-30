import tests.test_controllers.mock_requests as mock_requests

from controllers.commits_controller import get_commits
from models.commits_model import CommitsList, Commit


def test_get_commits_success():
    """Test get_commits() method for a successful response."""
    expected = CommitsList(commits=[
        Commit(sha="some_sha1"),
        Commit(sha="some_sha2")
    ])

    # * Setup mock request and response
    mock_requests.mock_response_func = lambda: mock_requests.MockCommitsResponse(
        status_code=200,
        response_key="MockCommitsResponse"
    )
    got = get_commits(
        owner="test_owner",
        repo="test_name",
        access_token="test_token",
        author='test_author',
        requests=mock_requests
    )

    assert len(got.commits) == 4
    assert got.commits[0].sha == expected.commits[0].sha
    assert got.commits[1].sha == expected.commits[1].sha
    assert got.commits[2].sha == expected.commits[0].sha
    assert got.commits[3].sha == expected.commits[1].sha


def test_get_commits_empty():
    """Test get_commits() method for an invalid status_code."""
    # * Setup mock request and response
    mock_requests.mock_response_func = lambda: mock_requests.MockCommitsResponse(
        status_code=401,
        response_key="MockCommitsResponse"
    )
    got = get_commits(
        owner="test_owner",
        repo="test_name",
        access_token="test_token",
        author='test_author',
        requests=mock_requests
    )

    assert not len(got.commits)
