import json

from models import collaborators_model

def test_collaborator():
    """
    Tests the creation and properties of a Collaborator object.

    This function creates a Collaborator object with sample data and asserts
    that the object's properties match the expected values. It checks the login
    property of the Collaborator object.
    """
    json_str = """
    {
        "login": "smungole"
    }
    """
    to_dict = json.loads(json_str)
    got = collaborators_model.Collaborator(**to_dict)
    expected = collaborators_model.Collaborator(login='smungole')

    assert isinstance(got, collaborators_model.Collaborator)
    assert got.login == expected.login


def test_collaborators():
    """
    Tests the creation and properties of a CollaboratorsList object.

    This function creates a CollaboratorsList object with sample data and asserts
    that the object's properties match the expected values. It checks the number of
    collaborators in the list and the login property of each Collaborator object
    within the list.
    """
    json_str = """
    {
        "collaborators": [
            {
                "login": "smungole"
            },
            {
                "login": "hsakhuja"
            }
        ]
    }
    """
    to_dict = json.loads(json_str)
    got = collaborators_model.CollaboratorsList(**to_dict)
    expected = collaborators_model.CollaboratorsList(collaborators=[
        collaborators_model.Collaborator(login='smungole'),
        collaborators_model.Collaborator(login='hsakhuja')
    ])

    assert isinstance(got, collaborators_model.CollaboratorsList)
    assert len(got.collaborators) == 2
    assert got.collaborators[0].login == expected.collaborators[0].login
    assert got.collaborators[1].login == expected.collaborators[1].login
