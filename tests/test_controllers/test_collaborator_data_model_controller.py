import tests.test_controllers.mock_collaborator_data_model_requests as mock_requests

from controllers.collaborator_data_model_controller import collaborator_individual_data_controller

from models.repository_io_model import RepositoryAnalysisIndividualInput
from models.collaborator_commit_model import IndividualCollaboratorCommit
from models.commit_details_model import CommitDetail
from models.pull_requests_model import PullRequests
from models.issues_model import Issue, User, Assignee


def test_collaborator_individual_data_controller_success():
    """
    Test the successful retrieval of collaborator data for an individual.

    This test checks if the collaborator_individual_data_controller function correctly processes input data and returns expected data.
    """
    input = RepositoryAnalysisIndividualInput(
        repository_owner="test1",
        repository_name="test_name",
        git_access_token="test_token",
        collaborator_username="test2"
    )
    expected = IndividualCollaboratorCommit(
        commits=[
            CommitDetail(sha="some_sha1"), 
            CommitDetail(sha="some_sha1")
        ],
        pr_created=[
            PullRequests(
                creator="test2",
                id=1143944226,
                pr_assignees=["test1", "test2"],
                created_at="2024-03-26T11:20:00Z",
                state="open"
            )
        ],
        pr_assigned=[
            PullRequests(
                creator="test1",
                id=1143972904,
                pr_assignees=["test1", "test2"],
                created_at="2022-12-03T03:33:04Z",
                closed_at="2022-12-03T03:33:55Z",
                state="closed"
            )
        ],
        issue_created=[],
        issue_assigned=[
            Issue(
                id=2203316067,
                user=User(login="test1"),
                assignee=Assignee(login="test2"),
                assignees=[
                    Assignee(login="test1"),
                    Assignee(login="test2")
                ],
                created_at="2024-03-22T20:57:28Z",
                updated_at="2024-03-22T20:57:28Z"
            )
        ]
    )

    mock_requests.mock_response_func = lambda url: mock_requests.mock_collaborator_data_model_response(
        status=200,
        url=url
    )
    got = collaborator_individual_data_controller(input, requests=mock_requests)

    assert got.commits[0].sha == expected.commits[0].sha
    assert got.commits[1].sha == expected.commits[1].sha

    assert len(got.pr_created) == len(expected.pr_created)
    assert got.pr_created[0].id == expected.pr_created[0].id
    assert len(got.pr_assigned) == len(expected.pr_assigned)
    assert got.pr_assigned[0].id == expected.pr_assigned[0].id

    assert len(got.issue_created) == len(expected.issue_created)
    assert len(got.issue_assigned) == len(expected.issue_assigned)
    assert got.issue_assigned[0].assignee.login == expected.issue_assigned[0].assignee.login


def test_collaborator_individual_data_controller_empty():
    """
    Test the scenario where the collaborator_individual_data_controller returns empty data.

    This test checks if the function correctly handles cases where the API response is empty or unauthorized.
    """
    input = RepositoryAnalysisIndividualInput(
        repository_owner="test1",
        repository_name="test_name",
        git_access_token="test_token",
        collaborator_username="test2"
    )

    mock_requests.mock_response_func = lambda url: mock_requests.mock_collaborator_data_model_response(
        status=401,
        url=url
    )
    got = collaborator_individual_data_controller(input, requests=mock_requests)

    assert len(got.commits) == 0
    assert len(got.pr_created) == 0
    assert len(got.pr_assigned) == 0
    assert len(got.issue_created) == 0
    assert len(got.issue_assigned) == 0
