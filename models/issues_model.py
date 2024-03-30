from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    login: str


class Assignee(BaseModel):
    login: str


class Issue(BaseModel):
    id: int
    user: User
    assignee: Optional[Assignee]
    assignees: List[Assignee]
    closed_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


class IssueList(BaseModel):
    issues: Optional[List[Issue]]
