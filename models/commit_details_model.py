from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel


class Author(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date: Optional[str]


class Committer(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date: Optional[str]


class Commit(BaseModel):
    url: Optional[str]
    author: Optional[Author]
    committer: Optional[Committer]
    message: Optional[str]


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
    patch: Optional[str]


class CommitDetail(BaseModel):
    url: Optional[str]
    sha: Optional[str]
    commit: Optional[Commit]
    stats: Optional[Stats]
    files: Optional[List[File]]
