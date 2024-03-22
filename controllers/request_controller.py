import logging
import os
import collections
import datetime

from models.collaborator_commit_model import CollaboratorCommitList, IndividualCollaboratorCommitList
from models.repository_io_model import RepositoryAnalysisIndividualOutputItem, RepositoryAnalysisOutputItem, RepositoryAnalysisOutputItemVerbose
from models.rules_model import ValidationRules
from models.collaborator_commit_model import CommitDetail
from utils.comments_utils import get_uncommented_lines
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("request_controller")


def get_bad_behaviour_report(info: CollaboratorCommitList, rules: ValidationRules) -> List[RepositoryAnalysisOutputItem]:
    log.info(f'rules: {rules}')
    report = [
        RepositoryAnalysisOutputItem(
            collaborator=item.collaborator.login, 
            violated_rules=[]
        ) for item in info.data
    ]
    collaborator_pr_count_dict = collections.defaultdict(int)
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

        for pr in item.pr_assigned:
            if pr_opened_in_last_sprint(pr.created_at):
                collaborator_pr_count_dict[item.collaborator.login] += 1

            # * 8. check violation for maxTimeToReviewPR
            td = pr_review_time(pr.created_at, pr.closed_at)
            if violated_max_time_to_review_pr(td, rules.maxTimeToReviewPR):
                report[index].violated_rules.append('maxTimeToReviewPR')

    # * 9. check violation for minPRToCreate
    for index, item in enumerate(info.data):
        if collaborator_pr_count_dict[item.collaborator.login] < rules.minPRToCreate:
            report[index].violated_rules.append('minPRToCreate')
    log.info(f'Generated report: {report}')
    return report


def get_bad_behaviour_report_verbose(info: CollaboratorCommitList, rules: ValidationRules) -> List[RepositoryAnalysisOutputItemVerbose]:
    log.info(f'rules: {rules}')
    report = [
        RepositoryAnalysisOutputItemVerbose(
            collaborator=item.collaborator.login, 
            violated_rules={}
        ) for item in info.data
    ]
    collaborator_pr_count_dict = collections.defaultdict(int)
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

        for pr in item.pr_assigned:
            if pr_opened_in_last_sprint(pr.created_at):
                collaborator_pr_count_dict[item.collaborator.login] += 1

            # * 8. check violation for maxTimeToReviewPR
            td = pr_review_time(pr.created_at, pr.closed_at)
            if violated_max_time_to_review_pr(td, rules.maxTimeToReviewPR):
                report[index].violated_rules['maxTimeToReviewPR'] = None

    # * 9. check violation for minPRToCreate
    for index, item in enumerate(info.data):
        if collaborator_pr_count_dict[item.collaborator.login] < rules.minPRToCreate:
            report[index].violated_rules['minPRToCreate'] = None

    log.info(f'Generated report: {report}')
    return report


def get_bad_behaviour_report_individual(info: IndividualCollaboratorCommitList, rules: ValidationRules) -> List[RepositoryAnalysisIndividualOutputItem]:
    pass


def violated_meaningful_lines_threshold(meaningful_lines: int, min_threshold: int) -> bool:
    return meaningful_lines < min_threshold


def violated_min_blame(additions: int, min_threshold: int) -> bool:
    return additions < min_threshold


def violated_min_lines(additions: int, deletions: int, min_threshold: int) -> bool:
    return additions - deletions < min_threshold


def violated_max_files_per_commit(extension_count: List[int], max_threshold: int) -> bool:
    return sum(extension_count) > max_threshold


def violated_allowed_file_types(extensions: List[str], allowed_file_types: set) -> bool:
    for ext in extensions:
        if ext not in allowed_file_types:
            return True
    return False


def violated_min_commits(commit_count: int, min_threshold: int) -> bool:
    """Gt number of commits for each developer"""
    return commit_count < min_threshold


def violated_min_time_between_commits(time_diffs: List[float], min_threshold: int) -> bool:
    return not all(map(lambda diff: diff >= min_threshold, time_diffs))


def violated_max_time_to_review_pr(review_time: float, max_threshold: int) -> bool:
    return review_time > max_threshold


def fetch_consecutive_time_between_commits(commits: List[CommitDetail]) -> List[float]:
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
    return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")


def time_difference(first: datetime.datetime, second: datetime.datetime) -> float:
    return (second - first).total_seconds() / 3600


def pr_review_time(created_at: str, closed_at: Optional[str]) -> float:
    pr_opened = to_datetime(created_at)
    if closed_at:
        pr_closed = to_datetime(closed_at)
    else:
        pr_closed = datetime.datetime.now(tz=pr_opened.tzinfo)

    return time_difference(pr_opened, pr_closed)

def pr_opened_in_last_sprint(created_at: str) -> bool:
    # Convert the created_at string to a datetime object
    pr_opened = to_datetime(created_at)
    
    # Calculate the date 14 days ago from today
    fourteen_days_ago = datetime.datetime.now() - datetime.timedelta(days=14)
    
    # Check if the PR was created in the last 14 days
    return pr_opened >= fourteen_days_ago

def calculate_time_diffs(timestamp_list: List[str]) -> List[float]:
    # Convert strings to datetime objects
    timestamps = [to_datetime(ts) for ts in timestamp_list[::-1]]
    # Calculate time differences in hours
    time_diffs = [
        time_difference(timestamps[i], timestamps[i + 1])
        for i in range(len(timestamps)-1)
    ]
    return list(reversed(time_diffs))


def get_meaningful_lines(commit_info: CommitDetail) -> int:
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
    stats = commit_info.stats
    if stats:
        additions = stats.additions or 0
        deletions = stats.deletions or 0
        return additions, deletions
    else:
        return 0, 0


def get_changed_files(commit_info: CommitDetail) -> dict:
    files = commit_info.files
    changed_files = [
        os.path.splitext(file.filename)[1]
        for file in files
    ]
    changed_files_extension = collections.Counter(changed_files)
    return changed_files_extension
