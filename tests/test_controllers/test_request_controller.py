from models.commit_details_model import CommitDetail, Commit, Author, Stats, File
from controllers import request_controller as rc


def test_violated_meaningful_lines_threshold():
    """
    Test the violated_meaningful_lines_threshold() function to ensure it correctly identifies if the
    meaningful lines threshold is violated.

    This test checks various scenarios where the actual meaningful lines are less than, equal to, or
    greater than the threshold. It verifies that the function returns True when the threshold is
    violated and False otherwise.

    Returns:
        None
    """
    assert rc.violated_meaningful_lines_threshold(5, 10)
    assert not rc.violated_meaningful_lines_threshold(10, 10)
    assert not rc.violated_meaningful_lines_threshold(10, 5)


def test_violated_min_blame():
    """
    Test the violated_min_blame() function to ensure it correctly identifies if the minimum blame
    threshold is violated.

    This test checks various scenarios where the actual blame is less than, equal to, or greater than
    the threshold. It verifies that the function returns True when the threshold is violated and
    False otherwise.

    Returns:
        None
    """
    assert rc.violated_min_blame(5, 10)
    assert not rc.violated_min_blame(10, 10)
    assert not rc.violated_min_blame(10, 5)


def test_violated_min_lines():
    """
    Test the violated_min_lines() function to ensure it correctly identifies if the minimum lines
    threshold is violated.

    This test checks various scenarios where the actual lines are less than, equal to, or greater than
    the threshold. It verifies that the function returns True when the threshold is violated and
    False otherwise.

    Returns:
        None
    """
    assert rc.violated_min_lines(5, 0, 10)
    assert not rc.violated_min_lines(15, 5, 10)
    assert not rc.violated_min_lines(15, 0, 10)


def test_violated_max_files_per_commit():
    """
    Test the violated_max_files_per_commit() function to ensure it correctly identifies if the maximum
    files per commit threshold is violated.

    This test checks various scenarios where the actual number of files per commit is less than, equal to,
    or greater than the threshold. It verifies that the function returns True when the threshold is
    violated and False otherwise.

    Returns:
        None
    """
    assert rc.violated_max_files_per_commit([1, 2, 3, 4], 5)
    assert not rc.violated_max_files_per_commit([1, 2, 3, 4], 10)
    assert not rc.violated_max_files_per_commit([2, 3], 10)


def test_violated_allowed_file_types():
    """
    Test the violated_allowed_file_types() function to ensure it correctly identifies if the allowed
    file types threshold is violated.

    This test checks various scenarios where the actual file types are within the allowed set or not.
    It verifies that the function returns True when the threshold is violated and False otherwise.

    Returns:
        None
    """
    assert rc.violated_allowed_file_types(['java', 'py'], set(['java']))
    assert not rc.violated_allowed_file_types(['java', 'py'], set(['java', 'py']))
    assert not rc.violated_allowed_file_types(['java'], set(['java', 'py']))


def test_violated_min_commits():
    """
    Test the violated_min_commits() function to ensure it correctly identifies if the minimum commits
    threshold is violated.

    This test checks various scenarios where the actual number of commits is less than, equal to, or
    greater than the threshold. It verifies that the function returns True when the threshold is
    violated and False otherwise.

    Returns:
        None
    """
    assert rc.violated_min_commits(5, 10)
    assert not rc.violated_min_commits(10, 10)
    assert not rc.violated_min_commits(10, 5)


def test_violated_min_time_between_commits():
    """
    Test the violated_min_time_between_commits() function to ensure it correctly identifies if the minimum
    time between commits threshold is violated.

    This test checks various scenarios where the actual time between commits is less than, equal to, or
    greater than the threshold. It verifies that the function returns True when the threshold is
    violated and False otherwise.

    Returns:
        None
    """
    assert rc.violated_min_time_between_commits([3, 4, 6, 8, 10], 6)
    assert not rc.violated_min_time_between_commits([3, 4, 6, 8, 10], 3)
    assert not rc.violated_min_time_between_commits([3, 4, 6, 8, 10], 1)


def test_violated_max_time():
    """
    Test the violated_max_time() function to ensure it correctly identifies if the maximum time
    threshold is violated.

    This test checks various scenarios where the actual time is less than, equal to, or greater than the
    threshold. It verifies that the function returns True when the threshold is violated and False
    otherwise.

    Returns:
        None
    """
    assert rc.violated_max_time(10, 5)
    assert not rc.violated_max_time(10, 10)
    assert not rc.violated_max_time(5, 5)


def test_to_datetime():
    """
    Test the to_datetime() function to ensure it correctly converts a string representation of a date
    and time to a datetime object.

    This test checks various scenarios where the input string is in different formats. It verifies that
    the function returns a datetime object with the correct year, month, day, hour, minute, and second.

    Returns:
        None
    """
    got = rc.to_datetime('2022-12-05T06:25:57Z')
    assert got.year == 2022
    assert got.month == 12
    assert got.day == 5
    assert got.hour == 6
    assert got.minute == 25
    assert got.second == 57


def test_time_difference():
    """
    Test the time_difference() function to ensure it correctly calculates the difference between two
    datetime objects.

    This test checks various scenarios where the two datetime objects represent different points in time.
    It verifies that the function returns the correct difference in hours.

    Returns:
        None
    """
    dt1 = rc.to_datetime('2022-12-05T06:00:00Z')
    dt2 = rc.to_datetime('2022-12-06T06:00:00Z')
    got = rc.time_difference(dt1, dt2)
    assert got == 24


def test_review_resolve_time():
    """
    Test the review_resolve_time() function to ensure it correctly calculates the time taken to resolve
    a review.

    This test checks various scenarios where the review start and end times are provided. It verifies that
    the function returns the correct time difference in hours.

    Returns:
        None
    """
    ts1 = '2022-12-05T07:00:00Z'
    ts2 = '2022-12-06T07:00:00Z'
    got = rc.review_resolve_time(ts1, ts2)
    assert got == 24

    got = rc.review_resolve_time(ts1, None)
    assert got > 24


def test_calculate_time_diffs():
    """
    Test the calculate_time_diffs() function to ensure it correctly calculates the time differences
    between consecutive timestamps.

    This test checks various scenarios where the input list of timestamps is in different orders and
    formats. It verifies that the function returns a list of time differences in hours.

    Returns:
        None
    """
    assert len(rc.calculate_time_diffs([])) == 0

    timestamps = [
        '2022-12-05T06:20:57Z',
        '2022-12-04T06:20:57Z',
        '2022-12-03T06:20:57Z',
        '2022-12-02T06:20:57Z',
    ]
    expected = [
        24.0,
        24.0,
        24.0
    ]
    assert expected == rc.calculate_time_diffs(timestamps)


def test_fetch_consecutive_time_between_commits():
    """
    Test the fetch_consecutive_time_between_commits() function to ensure it correctly calculates the time
    differences between consecutive commits.

    This test checks various scenarios where the input list of commits is in different orders and
    formats. It verifies that the function returns a list of time differences in hours.

    Returns:
        None
    """
    assert len(rc.fetch_consecutive_time_between_commits([])) == 0

    timestamps = [
        '2022-12-05T06:20:57Z',
        '2022-12-04T06:20:57Z',
        '2022-12-03T06:20:57Z',
        '2022-12-02T06:20:57Z',
    ]
    commits = [
        CommitDetail(commit=Commit(author=Author(date=date)))
        for date in timestamps
    ]
    expected = [
        24.0,
        24.0,
        24.0
    ]
    assert expected == rc.fetch_consecutive_time_between_commits(commits)


def test_get_number_of_new_lines():
    """
    Test the get_number_of_new_lines() function to ensure it correctly calculates the number of new lines
    added and deleted in a commit.

    This test checks various scenarios where the commit information includes different numbers of additions
    and deletions. It verifies that the function returns the correct number of new lines added and
    deleted.

    Returns:
        None
    """
    commit_info = CommitDetail(stats=Stats(additions=10, deletions=5))
    expected = 10, 5
    assert expected == rc.get_number_of_new_lines(commit_info)

    commit_info = CommitDetail()
    expected = 0, 0
    assert expected == rc.get_number_of_new_lines(commit_info)


def test_get_changed_files():
    """
    Test the get_changed_files() function to ensure it correctly identifies the types of files changed
    in a commit.

    This test checks various scenarios where the commit information includes different file types. It
    verifies that the function returns a dictionary with the correct count of each file type changed.

    Returns:
        None
    """
    commit_info = CommitDetail(files=[File(filename='test.py')])
    got = rc.get_changed_files(commit_info)
    assert len(got) == 1
    assert sum(got.values()) == 1
    assert got['.py'] == 1

    commit_info = CommitDetail(files=[
        File(filename='test1.py'),
        File(filename='test.java'),
        File(filename='test2.py')
    ])
    got = rc.get_changed_files(commit_info)
    assert len(got) == 2
    assert sum(got.values()) == 3
    assert got['.py'] == 2
    assert got['.java'] == 1


# def test_get_meaningful_lines():
#     commit_info = CommitDetail(files=[
#         File(
#             filename='test.py',
#             patch='+# greet\n+print("Hello, World!")'
#         )
#     ])
#     expected = 1
#     assert expected == rc.get_meaningful_lines(commit_info)
