from pydantic import BaseModel
from typing import List


class RepositoryAnalysisInput(BaseModel):
    repository_owner: str
    repository_name: str
    git_access_token: str


class ValidationRules(BaseModel):
    meaningfulLinesThreshold: int
    minCommits: int
    minLines: int
    minBlame: int
    minTimeBetweenCommits: int
    maxFilesPerCommit: int
    allowedFileTypes: List[str]

# "meaningfulLinesThreshold" : 5, // The minimum number of (non-comment) lines a commit must have in order to be considered meaningful
# "minCommits" : 3, // The minimum number of meaningful commits a developer is expected to make
# "minLines" : 0, // The minimum number of lines of code the developer is expected to have added overall
# "minBlame" : 3, // The minimum number of lines of code that should show a given developer in the Git Blame after making their commit
# "minTimeBetweenCommits" : 2, // The minimum amount of time (in hours) a developer is expected to wait between making commits (rapid fire commits are suspicious)
# "maxFilesPerCommit" : 3, // The maximum number of files a developer is expected to edit per commit
# "allowedFileTypes" : [ // Which file types developers are expected to commit - if blank allow all file types
#     ".java"
# ]
