from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Collaborator(BaseModel):
    login: str


class CollaboratorsList(BaseModel):
    collaborators: List[Collaborator]
