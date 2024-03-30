from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel

from .collaborators_model import Collaborator
from .commit_details_model import CommitDetail
from .pull_requests_model import PullRequests
from .issues_model import Issue


class CollaboratorCommit(BaseModel):
    collaborator: Collaborator
    commits: List[CommitDetail]
    pr_created: Optional[List[PullRequests]]
    pr_assigned: Optional[List[PullRequests]]
    issue_created: Optional[List[Issue]]
    issue_assigned: Optional[List[Issue]]


class CollaboratorCommitList(BaseModel):
    data: List[CollaboratorCommit]


class IndividualCollaboratorCommit(BaseModel):
    commits: List[CommitDetail]
    pr_created: Optional[List[PullRequests]]
    pr_assigned: Optional[List[PullRequests]]
    issue_created: Optional[List[Issue]]
    issue_assigned: Optional[List[Issue]]
