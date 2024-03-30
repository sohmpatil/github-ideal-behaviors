import json

from models import commits_model


def test_commits_list_model():
    json_str = """
    {
        "commits": [
            {
              "sha" : "some_sha1"  
            },
            {
              "sha" : "some_sha2"  
            }
        ]
    }
    """

    to_dict = json.loads(json_str)
    got = commits_model.CommitsList(**to_dict)
    expected = commits_model.CommitsList(
        commits=[
            commits_model.Commit(sha="some_sha1"),
            commits_model.Commit(sha="some_sha2")
        ]
    )
    assert isinstance(got, commits_model.CommitsList)
    assert len(expected.commits) == len(got.commits)
