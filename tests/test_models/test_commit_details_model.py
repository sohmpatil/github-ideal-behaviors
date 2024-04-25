import json

from models import commit_details_model

def test_commit_details():
    """
    Tests the creation and properties of a CommitDetail object.

    This function creates a CommitDetail object with sample data and asserts
    that the object's properties match the expected values. It checks the commit's
    SHA, author's name, the number of files changed, and the details of the first file.
    """
    json_str = r"""
    {
        "url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
        "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
        "commit": {
            "url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
            "author": {
                "name": "Monalisa Octocat",
                "email": "mona@github.com",
                "date": "2011-04-14T16:00:49Z"
            },
            "committer": {
                "name": "Monalisa Octocat",
                "email": "mona@github.com",
                "date": "2011-04-14T16:00:49Z"
            },
            "message": "Fix all the bugs"
        },
        "stats": {
            "additions": 104,
            "deletions": 4,
            "total": 108
        },
        "files": [
            {
                "filename": "file1.txt",
                "additions": 10,
                "deletions": 2,
                "changes": 12,
                "status": "modified",
                "patch": "@@ -29,7 +29,7 @@\n....."
            }
        ]
    }
    """
    to_dict = json.loads(json_str)
    from pprint import pprint
    pprint(to_dict)
    got = commit_details_model.CommitDetail(**to_dict)
    
    assert isinstance(got, commit_details_model.CommitDetail)
    assert got.sha == "6dcb09b5b57875f334f61aebed695e2e4193db5e"
    assert got.commit.author.name == "Monalisa Octocat"
    assert len(got.files) == 1
    assert got.files[0].filename == "file1.txt"
    