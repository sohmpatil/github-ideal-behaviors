import tests.test_controllers.mock_requests as mock_requests

from controllers.collaborators_controller import get_collaborators
from models.collaborators_model import CollaboratorsList, Collaborator


def test_get_collaborators_success():
    """
    Test the get_collaborators() method to ensure it successfully retrieves a list of collaborators.

    This test case mocks a successful response from the GitHub API and checks if the method correctly
    parses the response and returns a CollaboratorsList object with the expected collaborators.

    Returns:
        None
    """
    expected = CollaboratorsList(collaborators=[
        Collaborator(login="smungole"),
        Collaborator(login="hsakhuja")
    ])

    # * Setup mock request and response
    mock_requests.mock_response_func = lambda: mock_requests.MockResponse(
        status_code=200,
        response_key="MockCollaboratorsResponse"
    )
    got = get_collaborators(
        repo_owner="test_owner",
        repo_name="test_name",
        access_token="test_token",
        requests=mock_requests
    )

    assert len(got.collaborators) == 2
    assert got.collaborators[0].login == expected.collaborators[0].login
    assert got.collaborators[1].login == expected.collaborators[1].login


def test_get_collaborators_empty():
    """
    Test the get_collaborators() method to ensure it handles an empty response correctly.

    This test case mocks a response with a 401 status code, simulating an unauthorized request. It checks
    if the method correctly handles this case and returns an empty CollaboratorsList object.

    Returns:
        None
    """
    mock_requests.mock_response_func = lambda: mock_requests.MockResponse(
        status_code=401,
        response_key="MockCollaboratorsResponse"
    )
    got = get_collaborators(
        repo_owner="test_owner",
        repo_name="test_name",
        access_token="test_token",
        requests=mock_requests
    )

    assert not len(got.collaborators)
