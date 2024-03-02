import json

from models import bad_boys

def test_repository_analysis_input():
    json_str = """
    {
        "repository_owner": "hardik", 
        "repository_name": "test_repo",
        "git_access_token": "some_access_token"
    }
    """
    got = bad_boys.RepositoryAnalysisInput(**json.loads(json_str))
    expected =  bad_boys.RepositoryAnalysisInput(
        repository_name="test_repo",
        repository_owner="hardik",
        git_access_token="some_access_token"
    )
    assert isinstance(got, bad_boys.RepositoryAnalysisInput)
    assert got.repository_name == expected.repository_name
    assert got.repository_owner == expected.repository_owner
    assert got.git_access_token == expected.git_access_token


def test_repository_analysis_output_item():
    item = bad_boys.RepositoryAnalysisOutputItem(
        collaborator="smungole",
        violated_rules=["minLines", "minBlame"]
    )
    got = item.model_dump()
    assert got['collaborator'] == 'smungole'
    assert len(got['violated_rules']) == 2
    assert got['violated_rules'][0] == "minLines"
    assert got['violated_rules'][1] == "minBlame"
    
    response =  json.dumps(got)
    assert isinstance(response, str)


def test_repository_analysis_output_items():
    items = [
        bad_boys.RepositoryAnalysisOutputItem(
            collaborator="smungole",
            violated_rules=["minLines", "minBlame"]
        ),
        bad_boys.RepositoryAnalysisOutputItem(
            collaborator="hsakhuja",
            violated_rules=["minTimeBetweenCommits", "allowedFileTypes", "maxFilesPerCommit"]
        )
    ]
    got = list(map(lambda item: item.model_dump(), items))
    
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