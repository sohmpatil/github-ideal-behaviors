import json

from models import commits_model


def test_commits_list_model():
    """
    Tests the creation and properties of a CommitsList object.

    This function creates a CommitsList object with sample data and asserts
    that the object's properties match the expected values. It checks the number of
    commits in the list and the SHA of each commit within the list.
    """
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
