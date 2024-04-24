from collections import defaultdict
from typing import DefaultDict, List
from pydantic import BaseModel


class RepositoryAnalysisInput(BaseModel):
    """
    Represents the input for analyzing a GitHub repository.

    Attributes:
    - repository_owner: The owner of the GitHub repository.
    - repository_name: The name of the GitHub repository.
    - git_access_token: The access token for accessing the GitHub repository.
    """
    repository_owner: str
    repository_name: str
    git_access_token: str


class RepositoryAnalysisIndividualInput(BaseModel):
    """
    Represents the input for analyzing a GitHub repository for an individual collaborator.

    Attributes:
    - repository_owner: The owner of the GitHub repository.
    - repository_name: The name of the GitHub repository.
    - git_access_token: The access token for accessing the GitHub repository.
    - collaborator_username: The GitHub username of the collaborator to analyze.
    """
    repository_owner: str
    repository_name: str
    git_access_token: str
    collaborator_username: str


class RepositoryAnalysisIndividualOutputItem(BaseModel):
    """
    Represents the output item for an individual collaborator's analysis.

    Attributes:
    - violated_rules: List of strings representing the rules violated by the collaborator.
    """
    violated_rules: List[str]


class RepositoryAnalysisOutputItem(BaseModel):
    """
    Represents the output item for a collaborator's analysis in a GitHub repository.

    Attributes:
    - collaborator: The GitHub username of the collaborator.
    - violated_rules: List of strings representing the rules violated by the collaborator.
    """
    collaborator: str
    violated_rules: List[str]


class RepositoryAnalysisOutputItemVerbose(BaseModel):
    """
    Represents the verbose output item for a collaborator's analysis in a GitHub repository.

    Attributes:
    - collaborator: The GitHub username of the collaborator.
    - violated_rules: A dictionary mapping rule names to lists of details about the violations.
    """
    collaborator: str
    violated_rules: DefaultDict[str, List[str]]

    def __init__(self, **data):
        super().__init__(**data)
        self.violated_rules = defaultdict(list)
