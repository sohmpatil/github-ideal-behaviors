from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel


class PullRequests(BaseModel):
    """
    Represents a pull request in a GitHub repository.

    Attributes:
    - creator: Optional username of the creator of the pull request.
    - id: The unique identifier of the pull request.
    - pr_assignees: Optional list of usernames of the assignees of the pull request.
    - created_at: Timestamp when the pull request was created.
    - closed_at: Optional timestamp when the pull request was closed.
    - state: The state of the pull request (e.g., open, closed).
    - merge_commit_sha: Optional SHA hash of the merge commit.
    """
    creator: Optional[str]
    id: int
    pr_assignees: Optional[List[str]]
    created_at: str
    closed_at: Optional[str]
    state: str
    merge_commit_sha: Optional[str]

    @classmethod
    def parse_obj(cls, obj):
        user = obj.get('user', {}).get('login', '')
        assignees = [
            assignee.get('login', '') for assignee in obj.get('assignees', [])
        ]
        return super().parse_obj({**obj, 'creator': user, 'pr_assignees': assignees})


class PullRequestsList(BaseModel):
    """
    Represents a list of PullRequests objects.

    Attributes:
    - pull_requests: List of PullRequests objects, each representing a pull request in a GitHub repository.
    """
    pull_requests: List[PullRequests]
