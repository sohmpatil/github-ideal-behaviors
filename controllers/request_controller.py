import logging
import os
import collections
import datetime

from models.collaborator_commit_model import CollaboratorCommitList, IndividualCollaboratorCommit
from models.repository_io_model import RepositoryAnalysisIndividualOutputItem, RepositoryAnalysisOutputItem, RepositoryAnalysisOutputItemVerbose
from models.rules_model import ValidationRules
from models.collaborator_commit_model import CommitDetail
from utils.comments_utils import get_uncommented_lines
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("request_controller")


def get_bad_behaviour_report(info: CollaboratorCommitList, rules: ValidationRules) -> List[RepositoryAnalysisOutputItem]:
    """
    Generates a report of bad behaviors based on the provided commit information and validation rules.

    Args:
        info (CollaboratorCommitList): A list of collaborator commit data.
        rules (ValidationRules): A set of validation rules to check against.

    Returns:
        List[RepositoryAnalysisOutputItem]: A list of output items detailing the bad behaviors found.
    """
    log.info('rules: %s', rules)
    report = [
        RepositoryAnalysisOutputItem(
            collaborator=item.collaborator.login, 
            violated_rules=[]
        ) for item in info.data
    ]
    collaborator_pr_count_dict = collections.defaultdict(int)
    collaborator_issue_count_dict = collections.defaultdict(int)
    for index, item in enumerate(info.data):
        # * 1. check violation for min commits rule per developer
        if violated_min_commits(len(item.commits), rules.minCommits):
            report[index].violated_rules.append('minCommits')

        allowed_file_types = set(rules.allowedFileTypes)
        for commit_info in item.commits:
            files_extension_dict = get_changed_files(commit_info)

            # * 2. check violation of allowed file types rule per commit
            if 'allowedFileTypes' not in report[index].violated_rules \
                and violated_allowed_file_types(files_extension_dict.keys(), allowed_file_types):
                report[index].violated_rules.append('allowedFileTypes')

            # * 3. check violation of max number of allowed files per commit
            if 'maxFilesPerCommit' not in report[index].violated_rules \
                and violated_max_files_per_commit(files_extension_dict.values(), rules.maxFilesPerCommit):
                report[index].violated_rules.append('maxFilesPerCommit')
            
            additions, deletions = get_number_of_new_lines(commit_info)
            # * 4. check violation for min lines added overall
            if 'minLines' not in report[index].violated_rules \
                and violated_min_lines(additions, deletions, rules.minLines):
                report[index].violated_rules.append('minLines')

            # * 5. check violation for min blame per commit
            if 'minBlame' not in report[index].violated_rules \
                and violated_min_blame(additions, rules.minBlame):
                report[index].violated_rules.append('minBlame')

            # * 6. check violation for meaningful lines per commit
            meaningful_lines = get_meaningful_lines(commit_info)
            if 'meaningfulLinesThreshold' not in report[index].violated_rules \
                and violated_meaningful_lines_threshold(meaningful_lines, rules.meaningfulLinesThreshold):
                report[index].violated_rules.append('meaningfulLinesThreshold')
            
        # * 7. check violation for minTimeBetweenCommits
        time_diffs = fetch_consecutive_time_between_commits(item.commits)
        if violated_min_time_between_commits(time_diffs, rules.minTimeBetweenCommits):
            report[index].violated_rules.append('minTimeBetweenCommits')

        for pr in item.pr_created:
            if pr_opened_in_last_sprint(pr.created_at):
                collaborator_pr_count_dict[item.collaborator.login] += 1

        # * 8. check violation for maxTimeToReviewPR
        for pr in item.pr_assigned:
            td = review_resolve_time(pr.created_at, pr.closed_at)
            if violated_max_time(td, rules.maxTimeToReviewPR):
                report[index].violated_rules.append('maxTimeToReviewPR')
        
        for issue in item.issue_created:
            if issue_opened_in_last_sprint(issue.created_at):
                collaborator_issue_count_dict[item.collaborator.login] += 1

        for issue in item.issue_assigned:
            td = review_resolve_time(issue.created_at, issue.closed_at)
            if violated_max_time(td, rules.maxTimeToResolveIssue):
                report[index].violated_rules.append('maxTimeToResolveIssue')

    # * 9. check violation for minPRToCreate
    for index, item in enumerate(info.data):
        if collaborator_pr_count_dict[item.collaborator.login] < rules.minPRToCreate:
            report[index].violated_rules.append('minPRToCreate')

    # * 10. check violation for maxIssuesOpened
    for index, item in enumerate(info.data):
        if collaborator_issue_count_dict[item.collaborator.login] > rules.maxIssuesOpened:
            report[index].violated_rules.append('maxIssuesOpened')
    log.info('Generated report: %s', report)
    return report


def get_bad_behaviour_report_verbose(info: CollaboratorCommitList, rules: ValidationRules) -> List[RepositoryAnalysisOutputItemVerbose]:
    """
    Generates a verbose report of bad behaviors based on the provided commit information and validation rules.

    Args:
        info (CollaboratorCommitList): A list of collaborator commit data. 
        rules (ValidationRules): A set of validation rules to check against. 

    Returns:
        List[RepositoryAnalysisOutputItemVerbose]: A list of verbose output items. Each item in the list
            corresponds to a collaborator and contains a dictionary of rules that the
            collaborator has violated, with specific commit hashes as evidence for each violation.

    Raises:
        None.
    """
    log.info('rules: %s', rules)
    report = [
        RepositoryAnalysisOutputItemVerbose(
            collaborator=item.collaborator.login, 
            violated_rules={}
        ) for item in info.data
    ]
    collaborator_pr_count_dict = collections.defaultdict(int)
    collaborator_issue_count_dict = collections.defaultdict(int)
    for index, item in enumerate(info.data):
        # * 1. check violation for min commits rule per developer
        if violated_min_commits(len(item.commits), rules.minCommits):
            report[index].violated_rules['minCommits'] = None

        allowed_file_types = set(rules.allowedFileTypes)
        for commit_info in item.commits:
            files_extension_dict = get_changed_files(commit_info)

            # * 2. check violation of allowed file types rule per commit
            if violated_allowed_file_types(files_extension_dict.keys(), allowed_file_types):
                log.info(commit_info.sha)
                report[index].violated_rules['allowedFileTypes'].append(commit_info.sha)


            # * 3. check violation of max number of allowed files per commit
            if violated_max_files_per_commit(files_extension_dict.values(), rules.maxFilesPerCommit):
                report[index].violated_rules['maxFilesPerCommit'].append(commit_info.sha)
            
            additions, deletions = get_number_of_new_lines(commit_info)
            # * 4. check violation for min lines added overall
            if violated_min_lines(additions, deletions, rules.minLines):
                report[index].violated_rules['minLines'].append(commit_info.sha)

            # * 5. check violation for min blame per commit
            if violated_min_blame(additions, rules.minBlame):
                report[index].violated_rules['minBlame'].append(commit_info.sha)

            # * 6. check violation for meaningful lines per commit
            meaningful_lines = get_meaningful_lines(commit_info)
            if violated_meaningful_lines_threshold(meaningful_lines, rules.meaningfulLinesThreshold):
                report[index].violated_rules['meaningfulLinesThreshold'].append(commit_info.sha)

        # * 7. check violation for minTimeBetweenCommits
        time_diffs = fetch_consecutive_time_between_commits(item.commits)
        if violated_min_time_between_commits(time_diffs, rules.minTimeBetweenCommits):
            report[index].violated_rules['minTimeBetweenCommits'] = None

        for pr in item.pr_created:
            if pr_opened_in_last_sprint(pr.created_at):
                collaborator_pr_count_dict[item.collaborator.login] += 1

        for issue in item.issue_created:
            if issue_opened_in_last_sprint(issue.created_at):
                collaborator_issue_count_dict[item.collaborator.login] += 1

        # * 8. check violation for maxTimeToReviewPR
        for pr in item.pr_assigned:
            td = review_resolve_time(pr.created_at, pr.closed_at)
            if violated_max_time(td, rules.maxTimeToReviewPR):
                report[index].violated_rules['maxTimeToReviewPR'] = None

        for issue in item.issue_assigned:
            td = review_resolve_time(issue.created_at, issue.closed_at)
            if violated_max_time(td, rules.maxTimeToResolveIssue):
                report[index].violated_rules['maxTimeToResolveIssue'] = None

    # * 9. check violation for minPRToCreate
    for index, item in enumerate(info.data):
        if collaborator_pr_count_dict[item.collaborator.login] < rules.minPRToCreate:
            report[index].violated_rules['minPRToCreate'] = None

    # * 10. check violation for maxIssuesOpened
    for index, item in enumerate(info.data):
        if collaborator_issue_count_dict[item.collaborator.login] > rules.maxIssuesOpened:
            report[index].violated_rules.append('maxIssuesOpened') 
    log.info('Generated report: %s', report)
    return report


def get_bad_behaviour_report_individual(info: IndividualCollaboratorCommit, rules: ValidationRules) -> RepositoryAnalysisIndividualOutputItem:
    """
    Generates an individual report of bad behaviors based on the provided commit information and validation rules for a single collaborator.

    Args:
        info (IndividualCollaboratorCommit): An object containing information about a collaborator's commits, pull requests, and issues.
        rules (ValidationRules): A set of validation rules to check against. These rules define the criteria for what constitutes bad behavior in the context of the
            repository's collaboration practices.

    Returns:
        RepositoryAnalysisIndividualOutputItem: An output item detailing the bad behaviors found for the specified collaborator. This includes a list of rules that the
            collaborator has violated.

    Raises:
        None.
    """
    report = RepositoryAnalysisIndividualOutputItem(
        violated_rules=[]
    )
    # * 1. check violation for min commits rule
    if violated_min_commits(len(info.commits), rules.minCommits):
            report.violated_rules.append("minCommits")
    allowed_file_types = set(rules.allowedFileTypes)
    for commit_info in info.commits:
        files_extension_dict = get_changed_files(commit_info)

        # * 2. check violation of allowed file types rule per commit
        if 'allowedFileTypes' not in report.violated_rules \
            and violated_allowed_file_types(files_extension_dict.keys(), allowed_file_types):
            report.violated_rules.append('allowedFileTypes')

        # * 3. check violation of max number of allowed files per commit
        if 'maxFilesPerCommit' not in report.violated_rules \
            and violated_max_files_per_commit(files_extension_dict.values(), rules.maxFilesPerCommit):
            report.violated_rules.append('maxFilesPerCommit')
        
        additions, deletions = get_number_of_new_lines(commit_info)
        # * 4. check violation for min lines added overall
        if 'minLines' not in report.violated_rules \
            and violated_min_lines(additions, deletions, rules.minLines):
            report.violated_rules.append('minLines')

        # * 5. check violation for min blame per commit
        if 'minBlame' not in report.violated_rules \
            and violated_min_blame(additions, rules.minBlame):
            report.violated_rules.append('minBlame')

        # * 6. check violation for meaningful lines per commit
        meaningful_lines = get_meaningful_lines(commit_info)
        if 'meaningfulLinesThreshold' not in report.violated_rules \
            and violated_meaningful_lines_threshold(meaningful_lines, rules.meaningfulLinesThreshold):
            report.violated_rules.append('meaningfulLinesThreshold')
    
    # * 7. check violation for minTimeBetweenCommits
    time_diffs = fetch_consecutive_time_between_commits(info.commits)
    if violated_min_time_between_commits(time_diffs, rules.minTimeBetweenCommits):
        report.violated_rules.append('minTimeBetweenCommits')
    
    pr_count = 0
    for pr in info.pr_created:
        if pr_opened_in_last_sprint(pr.created_at):
            pr_count += 1
    
    issue_count = 0
    for issue in info.issue_created:
        if issue_opened_in_last_sprint(issue.created_at):
            issue_count += 1
    
    # * 8. check violation for maxTimeToReviewPR
    for pr in info.pr_assigned:
        td = review_resolve_time(pr.created_at, pr.closed_at)
        if violated_max_time(td, rules.maxTimeToReviewPR):
            report.violated_rules.append('maxTimeToReviewPR')

    for issue in info.issue_assigned:
        td = review_resolve_time(issue.created_at, issue.closed_at)
        if violated_max_time(td, rules.maxTimeToResolveIssue):
            report.violated_rules.append('maxTimeToResolveIssue')

    # * 9. check violation for minPRToCreate
    if pr_count < rules.minPRToCreate:
        report.violated_rules.append('minPRToCreate')

    # * 10. check violation for maxIssuesOpened
    if issue_count > rules.maxIssuesOpened:
        report.violated_rules.append('maxIssuesOpened')
        
    return report

def violated_meaningful_lines_threshold(meaningful_lines: int, min_threshold: int) -> bool:
    """
    Checks if the number of meaningful lines in a commit is below a specified minimum threshold.

    Args:
        meaningful_lines (int): The number of meaningful lines in a commit.
        min_threshold (int): The minimum threshold for meaningful lines.

    Returns:
        bool: True if the number of meaningful lines is below the minimum threshold, False otherwise.
    """
    return meaningful_lines < min_threshold


def violated_min_blame(additions: int, min_threshold: int) -> bool:
    """
    Checks if the number of blames in a commit is below a specified minimum threshold.

    Args:
        additions (int): The number of additions in a commit.
        min_threshold (int): The minimum threshold for additions.

    Returns:
        bool: True if the number of blames is below the minimum threshold, False otherwise.
    """
    return additions < min_threshold


def violated_min_lines(additions: int, deletions: int, min_threshold: int) -> bool:
    """
    Checks if the net number of lines added (additions minus deletions) in a commit is below a specified minimum threshold.

    Args:
        additions (int): The number of lines added in a commit.
        deletions (int): The number of lines deleted in a commit.
        min_threshold (int): The minimum threshold for net lines added.

    Returns:
        bool: True if the net number of lines added is below the minimum threshold, False otherwise.
    """
    return additions - deletions < min_threshold


def violated_max_files_per_commit(extension_count: List[int], max_threshold: int) -> bool:
    """
    Checks if the total number of files changed in a commit exceeds a specified maximum threshold.

    Args:
        extension_count (List[int]): A list of counts for each file extension changed in a commit.
        max_threshold (int): The maximum threshold for the total number of files changed.

    Returns:
        bool: True if the total number of files changed exceeds the maximum threshold, False otherwise.
    """
    return sum(extension_count) > max_threshold


def violated_allowed_file_types(extensions: List[str], allowed_file_types: set) -> bool:
    """
    Checks if any of the changed file types in a commit are not in the allowed file types set.

    Args:
        extensions (List[str]): A list of file extensions for files changed in a commit.
        allowed_file_types (set): A set of allowed file types.

    Returns:
        bool: True if any changed file type is not in the allowed file types set, False otherwise.
    """
    for ext in extensions:
        if ext not in allowed_file_types:
            return True
    return False


def violated_min_commits(commit_count: int, min_threshold: int) -> bool:
    """
    Checks if the number of commits by a collaborator is below a specified minimum threshold.

    Args:
        commit_count (int): The number of commits by a collaborator.
        min_threshold (int): The minimum threshold for the number of commits.

    Returns:
        bool: True if the number of commits is below the minimum threshold, False otherwise.
    """
    return commit_count < min_threshold


def violated_min_time_between_commits(time_diffs: List[float], min_threshold: int) -> bool:
    """
    Checks if the minimum time difference between consecutive commits is below a specified threshold.

    Args:
        time_diffs (List[float]): A list of time differences in hours between consecutive commits.
        min_threshold (int): The minimum threshold for the time difference between consecutive commits.

    Returns:
        bool: True if any time difference is below the minimum threshold, False otherwise.
    """

    return not all(map(lambda diff: diff >= min_threshold, time_diffs))


def violated_max_time(review_time: float, max_threshold: int) -> bool:
    """
    Checks if the review time for a pull request or issue exceeds a specified maximum threshold.

    Args:
        review_time (float): The review time in hours.
        max_threshold (int): The maximum threshold for the review time.

    Returns:
        bool: True if the review time exceeds the maximum threshold, False otherwise.
    """
    return review_time > max_threshold


def fetch_consecutive_time_between_commits(commits: List[CommitDetail]) -> List[float]:
    """
    Fetches the time differences in hours between consecutive commits.

    Args:
        commits (List[CommitDetail]): A list of commit details.

    Returns:
        List[float]: A list of time differences in hours between consecutive commits.
    """
    timestamp_list = []
    for commit_info in commits:
        commit_timestamp = commit_info.commit.author.date
        timestamp_list.append(commit_timestamp)

    if timestamp_list:
        time_diffs = calculate_time_diffs(timestamp_list)
        return time_diffs
    else:
        return []
    

def to_datetime(timestamp: str) -> datetime.datetime:
    """
    Converts a timestamp string to a datetime object.

    Args:
        timestamp (str): A timestamp string in the format "%Y-%m-%dT%H:%M:%SZ".

    Returns:
        datetime.datetime: A datetime object representing the given timestamp.
    """

    return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")


def time_difference(first: datetime.datetime, second: datetime.datetime) -> float:
    """
    Calculates the time difference in hours between two datetime objects.

    Args:
        first (datetime.datetime): The first datetime object.
        second (datetime.datetime): The second datetime object.

    Returns:
        float: The time difference in hours between the two datetime objects.
    """
    return (second - first).total_seconds() / 3600


def review_resolve_time(created_at: str, closed_at: Optional[str]) -> float:
    """
    Calculates the time taken to resolve a review (e.g., pull request or issue) in hours.

    Args:
        created_at (str): The timestamp when the review was created.
        closed_at (Optional[str]): The timestamp when the review was closed. If not provided,
            the current time is used.

    Returns:
        float: The time taken to resolve the review in hours.
    """

    pr_opened = to_datetime(created_at)
    if closed_at:
        pr_closed = to_datetime(closed_at)
    else:
        pr_closed = datetime.datetime.now(tz=pr_opened.tzinfo)

    return time_difference(pr_opened, pr_closed)

def pr_opened_in_last_sprint(created_at: str) -> bool:
    """
    Checks if a pull request was opened in the last 14 days.

    Args:
        created_at (str): The timestamp when the pull request was created.

    Returns:
        bool: True if the pull request was opened in the last 14 days, False otherwise.
    """
    # Convert the created_at string to a datetime object
    pr_opened = to_datetime(created_at)
    
    # Calculate the date 14 days ago from today
    fourteen_days_ago = datetime.datetime.now() - datetime.timedelta(days=14)
    
    # Check if the PR was created in the last 14 days
    return pr_opened >= fourteen_days_ago

def issue_opened_in_last_sprint(created_at: str) -> bool:
    """
    Checks if an issue was opened in the last 14 days.

    Args:
        created_at (str): The timestamp when the issue was created.

    Returns:
        bool: True if the issue was opened in the last 14 days, False otherwise.
    """
    # Convert the created_at string to a datetime object
    issue_opened = to_datetime(created_at)
    
    # Calculate the date 14 days ago from today
    fourteen_days_ago = datetime.datetime.now() - datetime.timedelta(days=14)
    
    # Check if the PR was created in the last 14 days
    return issue_opened >= fourteen_days_ago

def calculate_time_diffs(timestamp_list: List[str]) -> List[float]:
    """
    Calculates the time differences in hours between consecutive timestamps in a list.

    Args:
        timestamp_list (List[str]): A list of timestamp strings.

    Returns:
        List[float]: A list of time differences in hours between consecutive timestamps.
    """
    # Convert strings to datetime objects
    timestamps = [to_datetime(ts) for ts in timestamp_list[::-1]]
    # Calculate time differences in hours
    time_diffs = [
        time_difference(timestamps[i], timestamps[i + 1])
        for i in range(len(timestamps)-1)
    ]
    return list(reversed(time_diffs))


def get_meaningful_lines(commit_info: CommitDetail) -> int:
    """
    Calculates the number of meaningful lines added in a commit.

    Args:
        commit_info (CommitDetail): Detailed information about a commit.

    Returns:
        int: The number of meaningful lines added in the commit.
    """
    added_lines_dict = {}
    for file in commit_info.files:
        if file.patch:
            patch_lines = file.patch.split('\n')
            added_lines = [line[1:] for line in patch_lines if line.startswith('+') and not line.startswith('+++')]
            added_lines_dict[file.filename] = '\n'.join(added_lines)

    meaningful_lines = 0
    for file_name, content in added_lines_dict.items():
        meaningful_lines += get_uncommented_lines(
            file_name, 
            content
        )
    return meaningful_lines


def get_number_of_new_lines(commit_info: CommitDetail) -> tuple:
    """
    Retrieves the number of lines added and deleted in a commit.

    Args:
        commit_info (CommitDetail): Detailed information about a commit.

    Returns:
        tuple: A tuple containing the number of lines added and deleted in the commit.
    """
    stats = commit_info.stats
    if stats:
        additions = stats.additions or 0
        deletions = stats.deletions or 0
        return additions, deletions
    else:
        return 0, 0


def get_changed_files(commit_info: CommitDetail) -> dict:
    """
    Retrieve information about changed files from a commit.

    Args:
        commit_info (CommitDetail): Detailed information about a commit.

    Returns:
        dict: A dictionary containing file extensions as keys and their counts as values,
            representing the number of times files with specific extension was changed in the commit.

    Raises:
        None.
    """
    files = commit_info.files
    changed_files = [
        os.path.splitext(file.filename)[1]
        for file in files
    ]
    changed_files_extension = collections.Counter(changed_files)
    return changed_files_extension
