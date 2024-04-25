import json

from typing import Any, Callable, Optional, Union


class MockResponse:
    """
    This class mocks the Response object from the requests module.
    
    Attributes:
        status_code (int): The HTTP status code of the response.
        response_key (str): The key used to retrieve the mock response from the _mock_response dictionary.
    """
    def __init__(self, status_code: int, response_key: str) -> None:
        """
        Initialize the MockResponse object with a status code and a response key.
        
        Args:
            status_code (int): The HTTP status code of the response.
            response_key (str): The key used to retrieve the mock response from the _mock_response dictionary.
        """
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
        "MockPullRequestsResponse": """
        [
            {
                "assignees": [
                    { "login": "test1" },
                    { "login": "test2" }
                ],
                "closed_at": "2022-12-03T03:33:55Z",
                "created_at": "2022-12-03T03:33:04Z",
                "id": 1143972904,
                "merge_commit_sha": "e89f7a33d84b4057b8cfe9074a8b38f45bcb7804",
                "state": "closed",
                "user": { "login": "rhish9h" }
            },
            {
                "assignees": [
                    { "login": "test1" }
                ],
                "created_at": "2024-03-26T11:20:00Z",
                "id": 1143944226,
                "state": "open",
                "user": { "login": "sanket8397" }
            }
        ]
        """,
        "MockIssuesResponse": r"""
        [
            {
                "id": 2203316067,
                "user": {
                    "login": "sanket8397"
                },
                "assignee": {
                    "login": "sanket8397"
                },
                "assignees": [
                    {
                        "login": "sanket8397"
                    },
                    {
                        "login": "sanikag123"
                    }
                ],
                "closed_at": null,
                "created_at": "2024-03-22T20:57:28Z",
                "updated_at": "2024-03-22T20:57:28Z"
            },
            {
                "id": 124,
                "user": {
                    "login": "test"
                },
                "assignee": null,
                "assignees": [],
                "closed_at": null,
                "created_at": "2024-03-21T11:45:00Z",
                "updated_at": "2024-03-23T09:20:00Z"
            }
        ]
        """,
        "MockCommitsResponse": """
        [
            {
                "sha" : "some_sha1"  
            },
            {
                "sha" : "some_sha2"  
            }
        ]
        """,
        "MockCommitDetailsResponse": r"""
        {
            "url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
            "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
            "commit": {
                "url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
                "author": {
                    "name": "Monalisa Octocat",
                    "email": "mona@github.com",
                    "date": "2011-04-14T16:00:49Z"
                },
                "committer": {
                    "name": "Monalisa Octocat",
                    "email": "mona@github.com",
                    "date": "2011-04-14T16:00:49Z"
                },
                "message": "Fix all the bugs"
            },
            "stats": {
                "additions": 104,
                "deletions": 4,
                "total": 108
            },
            "files": [
                {
                    "filename": "file1.txt",
                    "additions": 10,
                    "deletions": 2,
                    "changes": 12,
                    "status": "modified",
                    "patch": "@@ -29,7 +29,7 @@\n....."
                }
            ]
        }
        """,
        "MockCollaboratorsResponse": """
        [
            {
                "login": "smungole"
            },
            {
                "login": "hsakhuja"
            }
        ]
        """
    }


class MockCommitsResponse(MockResponse):
    """
    This class extends MockResponse to mock the response of a commits API call.
    
    Attributes:
        curr_page (int): The current page of the paginated response.
        total_pages (int): The total number of pages in the paginated response.
    """
    curr_page = 0
    total_pages = 2

    def json(self) -> Any:
        """
        Returns the JSON content of the response, handling pagination.
        
        Returns:
            Any: The JSON content of the response.
        """
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
mock_response_func = lambda: MockResponse(200, "MockPullRequestsResponse")
mock_response = mock_response_func()
print(mock_response.status_code)
print(mock_response.json())
```
"""
mock_response_func: Optional[Callable[[], MockResponse]] = None


def get(url: str, headers: dict[str, str]) -> Union[MockResponse, None]:
    """
    Mocks the requests.get() method.
    
    Args:
        url (str): The URL of the API call.
        headers (dict[str, str]): The headers to be sent with the request.
        
    Returns:
        Union[MockResponse, None]: The mocked response object or None if no mock response function is set.
    """
    _ = url, headers
    if mock_response_func:
        return mock_response_func()
    return None
