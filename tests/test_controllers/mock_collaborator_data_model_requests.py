import json

from typing import Any, Union, Optional, Callable


class MockCollaboratorDataModelResponse:
    """
    This class mocks the Response object from the requests module.
    
    Attributes:
        status_code (int): The HTTP status code of the response.
        response_key (str): The key used to retrieve the mock response from the _mock_response dictionary.
    """
    def __init__(self, status_code: int, response_key: str) -> None:
        self.status_code = status_code
        self.response_key = response_key

    def json(self) -> Any:
        """
        Returns the JSON content of the response.
        
        Returns:
            Any: The JSON content of the response.
        """
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
                    "login": "test2"
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
        {
            "sha" : "some_sha1"  
        }
        """
    }
    

def mock_collaborator_data_model_response(status: int, url: str) -> MockCollaboratorDataModelResponse:
    """
    Mocks the response of an API call based on the URL.
    
    Args:
        url (str): The URL of the API call.
        
    Returns:
        MockCollaboratorDataModelResponse: The mocked response object.
    """
    url_path = url.split("?")[0]
    if url_path.endswith("collaborators"):
        # Return mock collaborators response
        return MockCollaboratorDataModelResponse(status, "collaborators")
    elif url_path.endswith("pulls"):
        # Return pull requests response
        return MockCollaboratorDataModelResponse(status, "pulls")
    elif url_path.endswith("issues"):
        # Return issues response
        return MockCollaboratorDataModelResponse(status, "issues")
    elif url_path.endswith("commits"):
        # Return commits list
        return MockCommitsResponse(status, "commits")
    else:
        # Return commit details
        return MockCollaboratorDataModelResponse(status, "details")


class MockCommitsResponse(MockCollaboratorDataModelResponse):
    curr_page = 0
    total_pages = 1

    def json(self) -> Any:
        if __class__.curr_page < __class__.total_pages:
            response = super()._mock_response.get(self.response_key)
            __class__.curr_page += 1
            return json.loads(response)
        else:
            __class__.curr_page = 0
            return json.loads('{}')


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
    """
    Mocks the requests.get() method.
    
    Args:
        url (str): The URL of the API call.
        headers (dict[str, str]): The headers to be sent with the request.
        
    Returns:
        Union[MockCollaboratorDataModelResponse, None]: The mocked response object or None if no mock response function is set.
    """
    _ = headers
    if mock_response_func:
        return mock_response_func(url)
    return None
