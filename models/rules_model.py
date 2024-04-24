from pydantic import BaseModel
from typing import List


class ValidationRules(BaseModel):
    """
    Represents the validation rules for analyzing GitHub repository behavior.

    Attributes:
    - meaningfulLinesThreshold: The threshold for meaningful lines of code.
    - minCommits: The minimum number of commits required.
    - minLines: The minimum number of lines of code required.
    - minBlame: The minimum number of blame lines required.
    - minTimeBetweenCommits: The minimum time between commits.
    - maxFilesPerCommit: The maximum number of files per commit.
    - allowedFileTypes: List of allowed file types.
    - minPRToCreate: The minimum number of pull requests to create.
    - maxTimeToReviewPR: The maximum time to review a pull request.
    - maxIssuesOpened: The maximum number of issues opened.
    - maxTimeToResolveIssue: The maximum time to resolve an issue.
    """
    meaningfulLinesThreshold: int
    minCommits: int
    minLines: int
    minBlame: int
    minTimeBetweenCommits: int
    maxFilesPerCommit: int
    allowedFileTypes: List[str]
    minPRToCreate: int
    maxTimeToReviewPR: int
    maxIssuesOpened: int
    maxTimeToResolveIssue: int
