import json

from typing import Any, Union, Optional, Callable


class MockCollaboratorDataModelResponse:
    """This mocks the Response object from requests module"""
    def __init__(self, status_code: int, response_key: str) -> None:
        self.status_code = status_code
        self.response_key = response_key

    def json(self) -> Any:
        response = __class__._mock_response.get(self.response_key)
        return json.loads(response)
    
    _mock_response: dict[str, str] = {
        "collaborators": """
        [
            {
                "login": "test1"
            },
            {
                "login": "test2"
            }
        ]
        """,
        "pulls": """
        [
            {
                "assignees": [
                    { "login": "test1" },
                    { "login": "test2" }
                ],
                "closed_at": "2022-12-03T03:33:55Z",
                "created_at": "2022-12-03T03:33:04Z",
                "id": 1143972904,
                "state": "closed",
                "user": { "login": "test1" }
            },
            {
                "assignees": [
                    { "login": "test1" }
                ],
                "created_at": "2024-03-26T11:20:00Z",
                "id": 1143944226,
                "state": "open",
                "user": { "login": "test2" }
            }
        ]
        """,
        "issues": r"""
        [
            {
                "id": 2203316067,
                "user": {
                    "login": "test1"
                },
                "assignee": {
                    "login": "test1"
                },
                "assignees": [
                    {
                        "login": "test1"
                    },
                    {
                        "login": "test2"
                    }
                ],
                "closed_at": null,
                "created_at": "2024-03-22T20:57:28Z",
                "updated_at": "2024-03-22T20:57:28Z"
            }
        ]
        """,
        "commits": """
        [
            {
                "sha" : "some_sha1"  
            },
            {
                "sha" : "some_sha2"  
            }
        ]
        """,
        "details": """
        [
            {
                "sha" : "some_sha1"  
            },
            {
                "sha" : "some_sha2"  
            }
        ]
        """
    }
    

def mock_collaborator_data_model_response(url: str) -> MockCollaboratorDataModelResponse:
    url_path = url.split("?")[0].endswith("commits")
    if url_path.endswith("collaborators"):
        # Return mock collaborators response
        return MockCollaboratorDataModelResponse(200, "collaborators")
    elif url_path.endswith("pulls"):
        # Return pull requests response
        return MockCollaboratorDataModelResponse(200, "pulls")
    elif url_path.endswith("issues"):
        # Return issues response
        return MockCollaboratorDataModelResponse(200, "issues")
    elif url_path.endswith("commits"):
        # Return commits list
        return MockCollaboratorDataModelResponse(200, "commits")
    else:
        # Return commit details
        return MockCollaboratorDataModelResponse(200, "details")
    

def mock_collaborator_data_model_error_response(url: str) -> MockCollaboratorDataModelResponse:
    _ = url
    return MockCollaboratorDataModelResponse(401, "issues")


"""
Use mock_response_func to setup the response of mock API call:
```python
# assign mock_collaborator_data_model_response func to receive mock response
mock_response_func = mock_collaborator_data_model_response
mock_url = "https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
mock_response = mock_response_func(mock_url)
print(mock_response.status_code)
print(mock_response.json())

# assign mock_collaborator_data_model_error_response func to receive error response
mock_response_func = mock_collaborator_data_model_error_response
mock_url = "https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
mock_response = mock_response_func(mock_url)
print(mock_response.status_code)
```
"""
mock_response_func: Optional[Callable[[str], MockCollaboratorDataModelResponse]] = None


def get(url: str, headers: dict[str, str]) -> Union[MockCollaboratorDataModelResponse, None]:
    """This mocks the requests.get() method"""
    _ = headers
    if mock_response_func:
        return mock_response_func(url)
    return None
