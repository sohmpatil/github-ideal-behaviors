from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel


class Author(BaseModel):
    """
    Represents the author of a commit.

    Attributes:
    - name: Optional name of the author.
    - email: Optional email of the author.
    - date: Optional date of the commit.
    """
    name: Optional[str]
    email: Optional[str]
    date: Optional[str]


class Committer(BaseModel):
    """
    Represents the committer of a commit.

    Attributes:
    - name: Optional name of the committer.
    - email: Optional email of the committer.
    - date: Optional date of the commit.
    """
    name: Optional[str]
    email: Optional[str]
    date: Optional[str]


class Commit(BaseModel):
    """
    Represents a commit in a GitHub repository.

    Attributes:
    - url: Optional URL to the commit.
    - author: Optional Author object containing author details.
    - committer: Optional Committer object containing committer details.
    - message: Optional commit message.
    """
    url: Optional[str]
    author: Optional[Author]
    committer: Optional[Committer]
    message: Optional[str]


class Stats(BaseModel):
    """
    Represents the statistics of a commit, such as additions, deletions, and total changes.

    Attributes:
    - additions: Optional number of additions in the commit.
    - deletions: Optional number of deletions in the commit.
    - total: Optional total number of changes in the commit.
    """    
    additions: Optional[int]
    deletions: Optional[int]
    total: Optional[int]


class File(BaseModel):
    """
    Represents a file changed in a commit.

    Attributes:
    - filename: Optional name of the file.
    - additions: Optional number of additions in the file.
    - deletions: Optional number of deletions in the file.
    - changes: Optional total number of changes in the file.
    - status: Optional status of the file (e.g., added, modified, deleted).
    - patch: Optional patch representing the changes to the file.
    """
    filename: Optional[str]
    additions: Optional[int]
    deletions: Optional[int]
    changes: Optional[int]
    status: Optional[str]
    patch: Optional[str]


class CommitDetail(BaseModel):
    """
    Represents detailed information about a commit, including the commit itself, stats, and files changed.

    Attributes:
    - url: Optional URL to the commit.
    - sha: Optional SHA hash of the commit.
    - commit: Optional Commit object containing author and committer details.
    - stats: Optional Stats object containing additions, deletions, and total changes.
    - files: Optional list of File objects representing the files changed in the commit.
    """    
    url: Optional[str]
    sha: Optional[str]
    commit: Optional[Commit]
    stats: Optional[Stats]
    files: Optional[List[File]]
