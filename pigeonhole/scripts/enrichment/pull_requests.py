import requests
from datetime import datetime, timedelta
import sys

def get_pr_analysis(self):
    """Get the number of pull requests and the acceptance rate of pull requests"""
    pr_analysis_dict = {
        "total_num_prs": 0,
        "pr_acceptance_rate_total": 0.0,
        "date_of_last_merged_pull_request": "None",
        "last_3_months": {
            "num_prs": 0,
            "num_prs_merged": 0,
            "pr_acceptance_rate_last_3_months": 0.0,
        },
        "last_6_months": {
            "num_prs": 0,
            "num_prs_merged": 0,
            "pr_acceptance_rate_last_6_months": 0.0,
        },
        "last_12_months": {
            "num_prs": 0,
            "num_prs_merged": 0,
            "pr_acceptance_rate_last_12_months": 0.0,
        }
    }

    try:
        query_params = {"state": "all", "per_page": 100, "page": 1}
        pulls_json = requests.get(self.base_url + "/pulls", headers=self.auth_headers, params=query_params).json()
        pr_analysis_dict["date_of_last_merged_pull_request"]  = datetime.strptime(pulls_json[0]["created_at"], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
        while pulls_json != [] and len(pulls_json) != 0:
            pr_analysis_dict["total_num_prs"] += len(pulls_json)
            for pull in pulls_json:
                created_at = datetime.strptime(pull["created_at"], '%Y-%m-%dT%H:%M:%SZ')
                state = pull["state"]
                merged_at = pull["merged_at"]
                # Count all pull requests and merged pull requests in the last 3, 6, and 12 months
                if state == "closed" and merged_at is not None:
                    if created_at > datetime.now() - timedelta(days=365):
                        pr_analysis_dict["last_12_months"]["num_prs"] += 1
                        pr_analysis_dict["last_12_months"]["num_prs_merged"] += 1
                    if created_at > datetime.now() - timedelta(days=180):
                        pr_analysis_dict["last_6_months"]["num_prs"] += 1
                        pr_analysis_dict["last_6_months"]["num_prs_merged"] += 1
                    if created_at > datetime.now() - timedelta(days=90):
                        pr_analysis_dict["last_3_months"]["num_prs"] += 1
                        pr_analysis_dict["last_3_months"]["num_prs_merged"] += 1
                elif state == "closed":
                    if created_at > datetime.now() - timedelta(days=365):
                        pr_analysis_dict["last_12_months"]["num_prs"] += 1
                    if created_at > datetime.now() - timedelta(days=180):
                        pr_analysis_dict["last_6_months"]["num_prs"] += 1
                    if created_at > datetime.now() - timedelta(days=90):
                        pr_analysis_dict["last_3_months"]["num_prs"] += 1
                else:
                    break

            query_params["page"] += 1
            pulls_json = requests.get(self.base_url + "/pulls", headers=self.auth_headers, params=query_params).json()

        # get the acceptance rate of pull requests
        if pr_analysis_dict["total_num_prs"] > 0:
            pr_analysis_dict["pr_acceptance_rate_total"] = pr_analysis_dict["total_num_prs"] / pr_analysis_dict["total_num_prs"]
            pr_analysis_dict["last_3_months"]["pr_acceptance_rate_last_3_months"] = (pr_analysis_dict["last_3_months"]["num_prs_merged"] / pr_analysis_dict["last_3_months"]["num_prs"]) if pr_analysis_dict["last_3_months"]["num_prs"] != 0 else 0
            pr_analysis_dict["last_6_months"]["pr_acceptance_rate_last_6_months"] = (pr_analysis_dict["last_6_months"]["num_prs_merged"] / pr_analysis_dict["last_6_months"]["num_prs"]) if pr_analysis_dict["last_6_months"]["num_prs"] != 0 else 0
            pr_analysis_dict["last_12_months"]["pr_acceptance_rate_last_12_months"] = (pr_analysis_dict["last_12_months"]["num_prs_merged"] / pr_analysis_dict["last_12_months"]["num_prs"]) if pr_analysis_dict["last_12_months"]["num_prs"] != 0 else 0
    
    except Exception as e:
        print("error: ", e)
        print("line number: ", sys.exc_info()[-1].tb_lineno)

    return pr_analysis_dict