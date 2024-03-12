from __future__ import annotations
from typing import Any, List, Optional
from pydantic import BaseModel

from .collaborators_model import Collaborator
from .commit_details_model import CommitDetail
from .pull_requests_model import PullRequestsList


class CollaboratorCommit(BaseModel):
    collaborator: Collaborator
    commits: List[CommitDetail]
    pr_created: Optional[List[PullRequestsList]]
    pr_assigned: Optional[List[PullRequestsList]]


class CollaboratorCommitList(BaseModel):
    data: List[CollaboratorCommit]
