from __future__ import annotations
from typing import Any, List, Optional
from pydantic import BaseModel

class Author(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date: Optional[str]

class Committer(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date: Optional[str]

class Tree(BaseModel):
    url: Optional[str]
    sha: Optional[str]

class Verification(BaseModel):
    verified: Optional[bool]
    reason: Optional[str]
    signature: Optional[Any]
    payload: Optional[Any]

class Commit(BaseModel):
    url: Optional[str]
    author: Optional[Author]
    committer: Optional[Committer]
    message: Optional[str]
    tree: Optional[Tree]
    comment_count: Optional[int]
    verification: Optional[Verification]

class Author1(BaseModel):
    login: Optional[str]
    id: Optional[int]
    node_id: Optional[str]
    avatar_url: Optional[str]
    gravatar_id: Optional[str]
    url: Optional[str]
    html_url: Optional[str]
    followers_url: Optional[str]
    following_url: Optional[str]
    gists_url: Optional[str]
    starred_url: Optional[str]
    subscriptions_url: Optional[str]
    organizations_url: Optional[str]
    repos_url: Optional[str]
    events_url: Optional[str]
    received_events_url: Optional[str]
    type: Optional[str]
    site_admin: Optional[bool]

class Committer1(BaseModel):
    login: Optional[str]
    id: Optional[int]
    node_id: Optional[str]
    avatar_url: Optional[str]
    gravatar_id: Optional[str]
    url: Optional[str]
    html_url: Optional[str]
    followers_url: Optional[str]
    following_url: Optional[str]
    gists_url: Optional[str]
    starred_url: Optional[str]
    subscriptions_url: Optional[str]
    organizations_url: Optional[str]
    repos_url: Optional[str]
    events_url: Optional[str]
    received_events_url: Optional[str]
    type: Optional[str]
    site_admin: Optional[bool]

class Parent(BaseModel):
    url: Optional[str]
    sha: Optional[str]

class Stats(BaseModel):
    additions: Optional[int]
    deletions: Optional[int]
    total: Optional[int]

class File(BaseModel):
    filename: Optional[str]
    additions: Optional[int]
    deletions: Optional[int]
    changes: Optional[int]
    status: Optional[str]
    raw_url: Optional[str]
    blob_url: Optional[str]
    patch: Optional[str]

class ModelItem(BaseModel):
    url: Optional[str]
    sha: Optional[str]
    node_id: Optional[str]
    html_url: Optional[str]
    comments_url: Optional[str]
    commit: Optional[Commit]
    author: Optional[Author1]
    committer: Optional[Committer1]
    parents: Optional[List[Parent]]
    stats: Optional[Stats]
    files: Optional[List[File]]

class SingleCommitModel(BaseModel):
    __root__: ModelItem
