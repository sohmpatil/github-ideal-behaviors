from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    """
    Represents a user in a GitHub repository.

    Attributes:
    - login: The GitHub login of the user.
    """
    login: str


class Assignee(BaseModel):
    """
    Represents an assignee in a GitHub repository.

    Attributes:
    - login: The GitHub login of the assignee.
    """
    login: str


class Issue(BaseModel):
    """
    Represents an issue in a GitHub repository.

    Attributes:
    - id: The unique identifier of the issue.
    - user: User object representing the user who created the issue.
    - assignee: Optional Assignee object representing the user assigned to the issue.
    - assignees: List of Assignee objects representing the users assigned to the issue.
    - closed_at: Optional timestamp when the issue was closed.
    - created_at: Optional timestamp when the issue was created.
    - updated_at: Optional timestamp when the issue was last updated.
    """
    id: int
    user: User
    assignee: Optional[Assignee]
    assignees: List[Assignee]
    closed_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


class IssueList(BaseModel):
    """
    Represents a list of Issue objects.

    Attributes:
    - issues: Optional list of Issue objects, each representing an issue in a GitHub repository.
    """
    issues: Optional[List[Issue]]
