import json

from models import repository_io_model

def test_repository_analysis_input():
    """
    Tests the creation and properties of a RepositoryAnalysisInput object.

    This function creates a RepositoryAnalysisInput object with sample data and asserts
    that the object's properties match the expected values. It checks the repository owner,
    repository name, and Git access token.
    """
    json_str = """
    {
        "repository_owner": "hardik", 
        "repository_name": "test_repo",
        "git_access_token": "some_access_token"
    }
    """
    got = repository_io_model.RepositoryAnalysisInput(**json.loads(json_str))
    expected =  repository_io_model.RepositoryAnalysisInput(
        repository_name="test_repo",
        repository_owner="hardik",
        git_access_token="some_access_token"
    )
    assert isinstance(got, repository_io_model.RepositoryAnalysisInput)
    assert got.repository_name == expected.repository_name
    assert got.repository_owner == expected.repository_owner
    assert got.git_access_token == expected.git_access_token


def test_repository_analysis_output_item():
    """
    Tests the creation and properties of a RepositoryAnalysisOutputItem object.

    This function creates a RepositoryAnalysisOutputItem object with sample data and asserts
    that the object's properties match the expected values. It checks the collaborator's name
    and the list of violated rules.
    """
    item = repository_io_model.RepositoryAnalysisOutputItem(
        collaborator="smungole",
        violated_rules=["minLines", "minBlame"]
    )
    got = item.dict()
    assert got['collaborator'] == 'smungole'
    assert len(got['violated_rules']) == 2
    assert got['violated_rules'][0] == "minLines"
    assert got['violated_rules'][1] == "minBlame"
    
    response =  json.dumps(got)
    assert isinstance(response, str)


def test_repository_analysis_output_items():
    """
    Tests the creation and properties of a list of RepositoryAnalysisOutputItem objects.

    This function creates a list of RepositoryAnalysisOutputItem objects with sample data and asserts
    that the list's properties match the expected values. It checks the number of items in the list,
    the collaborator's name, and the list of violated rules for each item.
    """
    items = [
        repository_io_model.RepositoryAnalysisOutputItem(
            collaborator="smungole",
            violated_rules=["minLines", "minBlame"]
        ),
        repository_io_model.RepositoryAnalysisOutputItem(
            collaborator="hsakhuja",
            violated_rules=["minTimeBetweenCommits", "allowedFileTypes", "maxFilesPerCommit"]
        )
    ]
    got = list(map(lambda item: item.dict(), items))
    
    assert len(got) == 2

    assert got[0]['collaborator'] == 'smungole'
    assert len(got[0]['violated_rules']) == 2
    assert got[0]['violated_rules'][0] == "minLines"
    assert got[0]['violated_rules'][1] == "minBlame"

    assert got[1]['collaborator'] == 'hsakhuja'
    assert len(got[1]['violated_rules']) == 3
    assert got[1]['violated_rules'][0] == "minTimeBetweenCommits"
    assert got[1]['violated_rules'][1] == "allowedFileTypes"
    assert got[1]['violated_rules'][2] == "maxFilesPerCommit"

    response =  json.dumps(got)
    assert isinstance(response, str)
