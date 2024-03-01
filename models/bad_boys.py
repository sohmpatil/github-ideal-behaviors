from typing import List
from pydantic import BaseModel


class RepositoryAnalysisInput(BaseModel):
    repository_owner: str
    repository_name: str
    git_access_token: str


class RepositoryAnalysisOutputItem(BaseModel):
    collaborator: str
    violated_rules: List[str]
