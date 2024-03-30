from models.commit_details_model import CommitDetail, Commit, Author, Stats, File
from controllers import request_controller as rc


def test_violated_meaningful_lines_threshold():
    assert rc.violated_meaningful_lines_threshold(5, 10)
    assert not rc.violated_meaningful_lines_threshold(10, 10)
    assert not rc.violated_meaningful_lines_threshold(10, 5)


def test_violated_min_blame():
    assert rc.violated_min_blame(5, 10)
    assert not rc.violated_min_blame(10, 10)
    assert not rc.violated_min_blame(10, 5)


def test_violated_min_lines():
    assert rc.violated_min_lines(5, 0, 10)
    assert not rc.violated_min_lines(15, 5, 10)
    assert not rc.violated_min_lines(15, 0, 10)


def test_violated_max_files_per_commit():
    assert rc.violated_max_files_per_commit([1, 2, 3, 4], 5)
    assert not rc.violated_max_files_per_commit([1, 2, 3, 4], 10)
    assert not rc.violated_max_files_per_commit([2, 3], 10)


def test_violated_allowed_file_types():
    assert rc.violated_allowed_file_types(['java', 'py'], set(['java']))
    assert not rc.violated_allowed_file_types(['java', 'py'], set(['java', 'py']))
    assert not rc.violated_allowed_file_types(['java'], set(['java', 'py']))


def test_violated_min_commits():
    assert rc.violated_min_commits(5, 10)
    assert not rc.violated_min_commits(10, 10)
    assert not rc.violated_min_commits(10, 5)


def test_violated_min_time_between_commits():
    assert rc.violated_min_time_between_commits([3, 4, 6, 8, 10], 6)
    assert not rc.violated_min_time_between_commits([3, 4, 6, 8, 10], 3)
    assert not rc.violated_min_time_between_commits([3, 4, 6, 8, 10], 1)


def test_violated_max_time():
    assert rc.violated_max_time(10, 5)
    assert not rc.violated_max_time(10, 10)
    assert not rc.violated_max_time(5, 5)


def test_to_datetime():
    got = rc.to_datetime('2022-12-05T06:25:57Z')
    assert got.year == 2022
    assert got.month == 12
    assert got.day == 5
    assert got.hour == 6
    assert got.minute == 25
    assert got.second == 57


def test_time_difference():
    dt1 = rc.to_datetime('2022-12-05T06:00:00Z')
    dt2 = rc.to_datetime('2022-12-06T06:00:00Z')
    got = rc.time_difference(dt1, dt2)
    assert got == 24


def test_review_resolve_time():
    ts1 = '2022-12-05T07:00:00Z'
    ts2 = '2022-12-06T07:00:00Z'
    got = rc.review_resolve_time(ts1, ts2)
    assert got == 24

    got = rc.review_resolve_time(ts1, None)
    assert got > 24


def test_calculate_time_diffs():
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
    commit_info = CommitDetail(stats=Stats(additions=10, deletions=5))
    expected = 10, 5
    assert expected == rc.get_number_of_new_lines(commit_info)

    commit_info = CommitDetail()
    expected = 0, 0
    assert expected == rc.get_number_of_new_lines(commit_info)


def test_get_changed_files():
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
