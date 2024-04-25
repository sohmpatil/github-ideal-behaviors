import json
from models import rules_model

def test_validation_rules():
    """
    Tests the creation and properties of a ValidationRules object.

    This function creates a ValidationRules object with sample data and asserts
    that the object's properties match the expected values. It checks various rules
    such as meaningful lines threshold, minimum commits, minimum lines, minimum blame,
    minimum time between commits, maximum files per commit, allowed file types, minimum
    pull requests to create, maximum time to review a pull request, maximum issues opened,
    and maximum time to resolve an issue.
    """
    json_str = r"""
    {
        "meaningfulLinesThreshold": 10,
        "minCommits": 5,
        "minLines": 100,
        "minBlame": 2,
        "minTimeBetweenCommits": 60,
        "maxFilesPerCommit": 5,
        "allowedFileTypes": ["py", "md"],
        "minPRToCreate": 2,
        "maxTimeToReviewPR": 720,
        "maxIssuesOpened": 10,
        "maxTimeToResolveIssue": 50
    }
    """
    to_dict = json.loads(json_str)
    from pprint import pprint
    pprint(to_dict)
    got = rules_model.ValidationRules(**to_dict)
    
    assert isinstance(got, rules_model.ValidationRules)
    assert got.meaningfulLinesThreshold == 10
    assert got.minCommits == 5
    assert got.minLines == 100
    assert got.minBlame == 2
    assert got.minTimeBetweenCommits == 60
    assert got.maxFilesPerCommit == 5
    assert got.allowedFileTypes == ["py", "md"]
    assert got.minPRToCreate == 2
    assert got.maxTimeToReviewPR == 720
    assert got.maxIssuesOpened == 10
    assert got.maxTimeToResolveIssue == 50
