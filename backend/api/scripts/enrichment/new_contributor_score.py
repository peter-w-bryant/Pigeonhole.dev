from datetime import datetime

def generate_new_contributor_score(self):
        """Generate a new contributor score"""
        try:
            score = 0
            # Number of stars
            num_stars = self.gh_stargazers_count
            if 0 <= num_stars <= 25:
                score += 20
            elif 25 < num_stars <= 50:
                score += 15
            elif 50 < num_stars <= 100:
                score += 10
            elif 100 < num_stars <= 500:
                score += 5
            elif 500 < num_stars <= 1000:
                score += 3
            elif 1000 < num_stars <= 2500:
                score += 2
            elif 2500 < num_stars <= 5000:
                score += 1
        
            # Number of Forks
            num_forks = self.gh_forks_count
            if 0 <= num_forks <= 5:
                score += 20
            elif 5 < num_forks <= 50:
                score += 15
            elif 50 < num_forks <= 100:
                score += 10
            elif 100 < num_forks <= 500:
                score += 5
            elif 500 < num_forks <= 1000:
                score += 3
            elif 1000 < num_forks <= 2500:
                score += 2
            elif 2500 < num_forks <= 5000:
                score += 1

            # Contains CONTRIBUTING.md
            if self.gh_contributing_url != "":
                score += 5

            # Issue Labels
            # label_score = 0
            # for label in self.gh_issues:
            #     if label in ["good first issue", "up-for-grabs", "easy to fix", "easy", "help wanted"] or "beginner" in label :
            #         label_count = self.gh_issues_dict[label]
            #         if 0 <= label_count <= 5:
            #             label_score += self.gh_issues_dict[label] * 0.25
            #         elif 5 < label_count <= 10:
            #             label_score += self.gh_issues_dict[label] * 0.1
            #         elif 10 < label_count <= 20:
            #             label_score += self.gh_issues_dict[label] * 0.05
            
            # if 10 < label_score:
            #     score += 10
            # else:
            #     score += label_score
            
            # Date of last merged PR
            if self.gh_date_of_last_merged_pull_request != "":
                date_last_pr = datetime.date(datetime.strptime(self.gh_date_of_last_merged_pull_request, "%Y-%m-%d")) 
                date_today = datetime.date(datetime.today())
                days_since_last_pr = abs((date_today - date_last_pr).days)
                if days_since_last_pr <= 7:
                    score += 3
                elif 7 < days_since_last_pr <= 14:
                    score += 2
                elif 14 < days_since_last_pr <= 30:
                    score += 1
                elif 30 <= days_since_last_pr <= 60:
                    score += 0.5
            max_score = 58
        except Exception as e:
            print("Error in generate_contrib_score:" ,e)
        return round((score/max_score) * 100, 2)