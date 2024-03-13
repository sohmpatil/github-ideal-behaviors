from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel


class PullRequests(BaseModel):
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
    pull_requests: List[PullRequests]
