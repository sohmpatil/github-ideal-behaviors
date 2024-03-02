import json5

from models import collaborators_model

def test_collaborator():
    json_str = """
    {
        "login": "smungole"
    }
    """
    to_dict = json5.loads(json_str)
    got = collaborators_model.Collaborator(**to_dict)
    expected = collaborators_model.Collaborator(login='smungole')

    assert isinstance(got, collaborators_model.Collaborator)
    assert got.login == expected.login


def test_collaborators():
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
    to_dict = json5.loads(json_str)
    got = collaborators_model.CollaboratorsList(**to_dict)
    expected = collaborators_model.CollaboratorsList(collaborators=[
        collaborators_model.Collaborator(login='smungole'),
        collaborators_model.Collaborator(login='hsakhuja')
    ])

    assert isinstance(got, collaborators_model.CollaboratorsList)
    assert len(got.collaborators) == 2
    assert got.collaborators[0].login == expected.collaborators[0].login
    assert got.collaborators[1].login == expected.collaborators[1].login
