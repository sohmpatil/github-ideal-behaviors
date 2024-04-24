from __future__ import annotations
from typing import List
from pydantic import BaseModel


class Commit(BaseModel):
    """
    Represents a commit in a GitHub repository.

    Attributes:
    - sha: The SHA hash of the commit.
    """
    sha: str


class CommitsList(BaseModel):
    """
    Represents a list of Commit objects.

    Attributes:
    - commits: List of Commit objects, each representing a commit in a GitHub repository.
    """
    commits: List[Commit]
