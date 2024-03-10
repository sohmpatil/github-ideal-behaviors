from controllers.pull_requests_controller import get_pull_requests
# import utils.github_utils as git_utils

import requests
from pprint import pprint

# repo_owner = 'sohmpatil'
# repo_name = 'github-ideal-behaviors'
repo_owner = 'sanket8397'
repo_name = 'CSE_564_Assignment_3_4'
access_token = "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"

t = get_pull_requests(repo_owner, repo_name, access_token)
for p in t.pull_requests:
    print(p)
