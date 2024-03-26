from pydantic import BaseModel
from typing import List

class ValidationRules(BaseModel):
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
