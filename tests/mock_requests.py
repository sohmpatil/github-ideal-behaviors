from typing import Any


class MockResponse:
    """This mocks the Response object from requests module"""

    def __init__(self, status_code: int, response: Any) -> None:
        self.status_code = status_code
        self.response = response

    def json(self) -> Any:
        return self.response
            

def get(url: str, headers: dict[str, str]) -> (MockResponse | None):
    """This mocks the requests.get() method"""
    _ = headers
    if url.rfind("pulls") != -1:
        return _mock_response.get("MockPullRequestsResponse")
    if url.endswith("issues"):
        return _mock_response.get("MockIssuesResponse")
    if url.split("?")[0].endswith("commits"):
        return _mock_response.get("MockCommitsResponse")
    if url.split("/")[-2] == "commits":
        return _mock_response.get("MockCommitDetailsResponse")
    if url.endswith("collaborators"):
        return _mock_response.get("MockCollaboratorsResponse")
    return None


_mock_response: dict[str, Any] = {
    "MockPullRequestsResponse": None,
    "MockIssuesResponse": None,
    "MockCommitsResponse": None,
    "MockCommitDetailsResponse": None,
    "MockCollaboratorsResponse": None
}
