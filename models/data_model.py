from pydantic import BaseModel
from typing import Dict, List

class RepositoryAnalysisInput(BaseModel):
    repository_owner: str
    repository_name: str
    git_access_token: str