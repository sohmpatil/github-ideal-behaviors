from __future__ import annotations
from typing import List
from pydantic import BaseModel


class Commit(BaseModel):
    sha: str


class CommitsList(BaseModel):
    commits: List[Commit]
