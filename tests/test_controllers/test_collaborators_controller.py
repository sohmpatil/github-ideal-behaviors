import tests.test_controllers.mock_requests as mock_requests

from controllers.collaborators_controller import get_collaborators
from models.collaborators_model import CollaboratorsList, Collaborator


def test_get_collaborators_success():
    """Test get_collaborators() method for a successful response."""
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
    """Test get_collaborators() method for an invalid status_code."""
    # * Setup mock request and response
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
