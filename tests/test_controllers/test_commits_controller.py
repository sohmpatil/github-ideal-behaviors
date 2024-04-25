import tests.test_controllers.mock_requests as mock_requests

from controllers.commits_controller import get_commits
from models.commits_model import CommitsList, Commit


def test_get_commits_success():
    """
    Test the get_commits() method to ensure it successfully retrieves a list of commits.

    This test case mocks a successful response from the GitHub API and checks if the method correctly
    parses the response and returns a CommitsList object with the expected commits. It verifies the
    length of the commits list and the SHA of each commit to ensure they match the expected values.

    Returns:
        None
    """
    expected = CommitsList(commits=[
        Commit(sha="some_sha1"),
        Commit(sha="some_sha2")
    ])
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
    """
    Test the get_commits() method to ensure it handles an empty response correctly.

    This test case mocks a response with a 401 status code, simulating an unauthorized request. It checks
    if the method correctly handles this case and returns an empty CommitsList object.

    Returns:
        None
    """
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
