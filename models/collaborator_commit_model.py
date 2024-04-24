from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel

from .collaborators_model import Collaborator
from .commit_details_model import CommitDetail
from .pull_requests_model import PullRequests
from .issues_model import Issue


class CollaboratorCommit(BaseModel):
    """
    Represents a collaborator's commit details, including commits, pull requests created/assigned, and issues created/assigned.

    Attributes:
    - collaborator: Collaborator object representing the collaborator.
    - commits: List of CommitDetail objects representing the commits made by the collaborator.
    - pr_created: Optional list of PullRequests objects representing the pull requests created by the collaborator.
    - pr_assigned: Optional list of PullRequests objects representing the pull requests assigned to the collaborator.
    - issue_created: Optional list of Issue objects representing the issues created by the collaborator.
    - issue_assigned: Optional list of Issue objects representing the issues assigned to the collaborator.
    """
    collaborator: Collaborator
    commits: List[CommitDetail]
    pr_created: Optional[List[PullRequests]]
    pr_assigned: Optional[List[PullRequests]]
    issue_created: Optional[List[Issue]]
    issue_assigned: Optional[List[Issue]]


class CollaboratorCommitList(BaseModel):
    """
    Represents a list of CollaboratorCommit objects.

    Attributes:
    - data: List of CollaboratorCommit objects, each representing a collaborator's commit details.
    """
    data: List[CollaboratorCommit]


class IndividualCollaboratorCommit(BaseModel):
    """
    Represents the commit details of an individual collaborator, including commits, pull requests created/assigned, and issues created/assigned.

    Attributes:
    - commits: List of CommitDetail objects representing the commits made by the collaborator.
    - pr_created: Optional list of PullRequests objects representing the pull requests created by the collaborator.
    - pr_assigned: Optional list of PullRequests objects representing the pull requests assigned to the collaborator.
    - issue_created: Optional list of Issue objects representing the issues created by the collaborator.
    - issue_assigned: Optional list of Issue objects representing the issues assigned to the collaborator.
    """
    commits: List[CommitDetail]
    pr_created: Optional[List[PullRequests]]
    pr_assigned: Optional[List[PullRequests]]
    issue_created: Optional[List[Issue]]
    issue_assigned: Optional[List[Issue]]
