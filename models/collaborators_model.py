from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Collaborator(BaseModel):
    """
    Represents a collaborator in a GitHub repository.

    Attributes:
    - login: The GitHub login of the collaborator.
    """
    login: str


class CollaboratorsList(BaseModel):
    """
    Represents a list of Collaborator objects.

    Attributes:
    - collaborators: List of Collaborator objects, each representing a collaborator in a GitHub repository.
    """
    collaborators: List[Collaborator]
