import requests

new_contrib_issue_list = ['good first issue', 'up-for-grabs', 'help wanted', 'easy to fix',
                          'easy', 'starter-task', 'contribution-starter', 'level:starter',
                          'newbie', 'beginner experience', 'beginners', 'beginner friendly',
                          'beginner-friendly-issues', 'beginner-task', 'difficulty:beginner',
                          'difficulty:easy', 'easy pick', 'easy-pickings', 'first-timers-only',
                          'junior job', 'needs help', 'learning opportunity', 'documentation',
                          'bug', 'enhancement', 'refactor', 'needs investigation', 'testing'
                          'minor', 'trivial']

def get_target_issues(self):
        """Gets all the open issue labels and the counts of all issue labels for a given repository.

        Returns:
        issue_label_counts(dict): a dictionary with keys corresponding to unique issue labels whose values are the count
        of open issues that have that label tag.
        """
        issue_label_counts = {}
        issue_id_lookup = {}

        for issue_label in new_contrib_issue_list:
            is_valid_page = True
            page = 0
            while is_valid_page:
                page += 1
                query_url = f"{self.base_url}/issues?state=open&per_page=100&page={page}&labels={issue_label}"
                issues_json = requests.get(query_url, headers=self.auth_headers).json()
                if issues_json == []:
                    if page != 1:
                        is_valid_page = False
                    break
                for issue in issues_json:
                    try:
                        if issue['id'] not in issue_id_lookup.keys():
                            issue_id_lookup[issue['id']] = True
                            # add only the issue labels that are in our list of new contributor issue labels
                            for i in range(len(issue['labels'])):
                                label_name = issue['labels'][i]['name'].lower()
                                # if the issue label is not in our dictionary, add it
                                if label_name not in issue_label_counts.keys():
                                    # if the issue label is in our list of new contributor issue labels or if it relates to bounties, add it
                                    if (label_name in new_contrib_issue_list):
                                        issue_label_counts[label_name] = 1
                                    elif('bounty' in label_name) or ('bounties' in label_name):
                                        self.gh_has_bounty_label = True
                                        issue_label_counts[label_name] = 1
                                # if the issue label is in our dictionary, increment the count
                                else:
                                    issue_label_counts[label_name] += 1
                    except Exception as e:
                        # print(e)
                        pass

        return get_issues_reorder_keys(self, issue_label_counts)
    
def get_issues_reorder_keys(self, issue_dict):
    """Reorders a dictionary of issue label count pairs so that our most important issue
    tags appear first. 
    Args:
    issue_dict(dict): a dictionary with keys corresponding to unique issue labels whose values are the count
    Returns:
    resorted_issue_dict(dict): a dictionary with keys corresponding to unique issue labels whose values are the count
    """
    resorted_issue_dict = {}
    for key in new_contrib_issue_list:
        if key in issue_dict.keys():
            resorted_issue_dict[key] = issue_dict[key]
    # add the rest of the keys
    for key in issue_dict.keys():
        if key not in resorted_issue_dict.keys():
            resorted_issue_dict[key] = issue_dict[key]        
    return resorted_issue_dict