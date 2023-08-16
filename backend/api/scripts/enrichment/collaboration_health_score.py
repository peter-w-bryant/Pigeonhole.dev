import requests
from datetime import datetime, timedelta

def generate_collaboration_health_score(self):
    repo_data = self.repo_data

    # Calculate metrics (same as before)
    commits_count = repo_data.get('commits_count', 0)  # Replace with actual commit count
    open_issues_count = repo_data.get('open_issues', 0)  # Replace with actual open issues count
    pr_acceptance_rate = repo_data.get('pr_acceptance_rate', 0.0)  # Replace with actual PR acceptance rate
    last_pushed_at = datetime.strptime(repo_data.get('pushed_at', ''), '%Y-%m-%dT%H:%M:%SZ')
 
    # print all the above
    print(f"commits_count: {commits_count}")
    print(f"open_issues_count: {open_issues_count}")
    print(f"pr_acceptance_rate: {pr_acceptance_rate}")
    print(f"last_pushed_at: {last_pushed_at}")

    # Calculate pull request merging time (same as before)
    pr_merge_time = timedelta(seconds=0)  # Replace with actual pull request merging time calculation

    # Calculate recent activity score based on the past 3 months
    activity_start_date = datetime.now() - timedelta(days=90)
    recent_commits = repo_data.get('commits', [])
    recent_commits_count = sum(1 for commit in recent_commits if datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') > activity_start_date)
    recent_activity_score = recent_commits_count / max(1, commits_count)

    # Evaluate number of comments and new issues in the past 3 months
    recent_issues = repo_data.get('issues', [])
    recent_issue_comments = sum(len(issue['comments']) for issue in recent_issues if datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ') > activity_start_date)
    new_issues_count = sum(1 for issue in recent_issues if datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ') > activity_start_date)

    # Calculate overall collaboration health score (same as before, adjusted weights)
    collaboration_health_score = (
        0.2 * self.gh_num_contributors +
        0.2 * commits_count +
        0.2 * (1 - open_issues_count / max(1, open_issues_count)) +
        0.1 * pr_acceptance_rate +
        0.1 * pr_merge_time.total_seconds() +
        0.15 * recent_activity_score +
        0.05 * (recent_issue_comments + new_issues_count)
    )

    return collaboration_health_score