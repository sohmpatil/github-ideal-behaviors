import logging
import os
import collections
import datetime

from models.final_model import CollaboratorCommitList
from models.bad_boys import RepositoryAnalysisOutputItem
from models.rules_model import ValidationRules
from models.final_model import CommitDetail
from utils.comments_utils import get_uncommented_lines
from typing import List

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

            # * 7. check violation of max number of allowed files per commit
            if 'maxFilesPerCommit' not in report[index].violated_rules \
                and violated_max_files_per_commit(files_extension_dict.values(), rules.maxFilesPerCommit):
                report[index].violated_rules.append('maxFilesPerCommit')
            
            additions, deletions = get_number_of_new_lines(commit_info)
            # * 3. check violation for min lines added overall
            if 'minLines' not in report[index].violated_rules \
                and violated_min_lines(additions, deletions, rules.minLines):
                report[index].violated_rules.append('minLines')

            # * 4. check violation for min blame per commit
            if 'minBlame' not in report[index].violated_rules \
                and violated_min_blame(additions, rules.minBlame):
                report[index].violated_rules.append('minBlame')

            # * 5. check violation for meaningful lines per commit
            meaningful_lines = get_meaningful_lines(commit_info)
            if 'meaningfulLinesThreshold' not in report[index].violated_rules \
                and violated_meaningful_lines_threshold(meaningful_lines, rules.meaningfulLinesThreshold):
                report[index].violated_rules.append('meaningfulLinesThreshold')

        # * 6. check violation for minTimeBetweenCommits
        time_diffs = fetch_consecutive_time_between_commits(item.commits)
        if violated_min_time_between_commits(time_diffs, rules.minTimeBetweenCommits):
            report[index].violated_rules.append('minTimeBetweenCommits')

    log.info(f'Generated report: {report}')
    return report


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


def calculate_time_diffs(timestamp_list: List[str]) -> List[float]:
    # Convert strings to datetime objects
    timestamps = [
        datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        for ts in timestamp_list[::-1]
    ]
    # Calculate time differences in hours
    time_diffs = [
        (timestamps[i+1] - timestamps[i]).total_seconds() / 3600
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
