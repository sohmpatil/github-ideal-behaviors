from collections import defaultdict
from typing import DefaultDict, List
from pydantic import BaseModel


class RepositoryAnalysisInput(BaseModel):
    repository_owner: str
    repository_name: str
    git_access_token: str


class RepositoryAnalysisIndividualInput(BaseModel):
    repository_owner: str
    repository_name: str
    git_access_token: str
    collaborator_username: str


class RepositoryAnalysisIndividualOutputItem(BaseModel):
    violated_rules: List[str]


class RepositoryAnalysisOutputItem(BaseModel):
    collaborator: str
    violated_rules: List[str]


class RepositoryAnalysisOutputItemVerbose(BaseModel):
    collaborator: str
    violated_rules: DefaultDict[str, List[str]]

    def __init__(self, **data):
        super().__init__(**data)
        self.violated_rules = defaultdict(list)
