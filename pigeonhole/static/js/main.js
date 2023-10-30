function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Add smooth scrolling animation
    });
}

window.addEventListener('scroll', () => {
    const button = document.getElementById('back-to-top-button');
    if (window.scrollY > 200) {
        button.style.display = 'block'; // Show the button when scroll position is greater than 200px
    } else {
        button.style.display = 'none'; // Hide the button when scroll position is less than 200px
    }
});

window.addEventListener('load', () => {

    // JavaScript to handle form submission and filtering projects from projects.json
    document.getElementById('search-form').addEventListener('input', (e) => {
        e.preventDefault();
        const searchQuery = document.getElementById('search-input').value;
        const projectContainer = document.getElementById('project-container');
        projectContainer.innerHTML = '';
        // Read in static_data/projects.json
        fetch('api/static_data/projects.json')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                console.log(data)
                // Data is a json object mapping github url to project dict
                // for key value pairs in data
                for (const [key, value] of Object.entries(data)) {
                    // If the project name contains the search query
                    if (value.repo_name.toLowerCase().includes(searchQuery.toLowerCase())) {
                        // Create a new project-square
                        const projectCard = document.createElement('div');
                        projectCard.className = 'project-square';

                        // START creating project top
                        const projectTop = document.createElement('div');
                        projectTop.className = 'project-top';
                        const projectName = document.createElement('a');
                        projectName.href = value.repo_url;
                        projectName.className = 'project-name';
                        projectName.innerText = value.repo_name;
                        projectTop.appendChild(projectName);

                        // Create CONTRIBUTING.md link if it exists
                        if (value.gh_contributing_url) {
                            const contributingLink = document.createElement('a');
                            contributingLink.className = 'project-label';
                            contributingLink.href = value.gh_contributing_url;
                            contributingLink.target = '_blank';
                            const contributingText = document.createElement('p');
                            contributingText.className = 'project-contributing-text';
                            contributingText.innerText = 'CONTRIBUTING.md';
                            const contributingIcon = document.createElement('i');
                            contributingIcon.className = 'fas fa-file-code';
                            contributingText.appendChild(contributingIcon);
                            contributingLink.appendChild(contributingText);
                            projectTop.appendChild(contributingLink);
                        }

                        // Create Bug Bounty link if it exists
                        if (value.gh_has_bounty_label) {
                            const bountyLink = document.createElement('a');
                            bountyLink.className = 'project-label';
                            bountyLink.href = value.gh_contributing_url;
                            bountyLink.target = '_blank';
                            const bountyText = document.createElement('p');
                            bountyText.className = 'project-contributing-text';
                            bountyText.innerText = 'Bug Bounty';
                            const bountyIcon = document.createElement('i');
                            bountyIcon.className = 'fas fa-bug';
                            bountyIcon.style.color = '#FFD700';
                            bountyText.appendChild(bountyIcon);
                            bountyLink.appendChild(bountyText);
                            projectTop.appendChild(bountyLink);
                        }

                        // Create github link
                        const githubLink = document.createElement('a');
                        githubLink.href = value.repo_url;
                        githubLink.target = '_blank';
                        const githubIcon = document.createElement('i');
                        githubIcon.className = 'fab fa-github github-icon';
                        githubLink.appendChild(githubIcon);
                        projectTop.appendChild(githubLink);

                        // Add project top to project card
                        projectCard.appendChild(projectTop);
                        // END creating project top

                        // START creating username container
                        const usernameContainer = document.createElement('div');
                        usernameContainer.className = 'username-container';
                        const usernameLink = document.createElement('a');
                        usernameLink.href = value.user_url;
                        usernameLink.className = 'project-username';
                        usernameLink.innerText = value.username;
                        usernameContainer.appendChild(usernameLink);
                        projectCard.appendChild(usernameContainer);
                        // END creating username container

                        // START creating project icons
                        const projectIcons = document.createElement('div');
                        projectIcons.className = 'project-icons';

                        // Add watchers
                        const viewsIcon = document.createElement('i');
                        viewsIcon.className = 'fas fa-eye views-icon';
                        viewsIcon.title = `${value.gh_watchers_count} Watchers`;
                        viewsIcon.innerText = value.gh_watchers_count;
                        projectIcons.appendChild(viewsIcon);

                        // Add forks
                        const forksIcon = document.createElement('i');
                        forksIcon.className = 'fas fa-code-branch forks-icon';
                        forksIcon.title = `${value.gh_forks_count} Forks`;
                        forksIcon.innerText = value.gh_forks_count;
                        projectIcons.appendChild(forksIcon);

                        // Add stargazers
                        const starsIcon = document.createElement('i');
                        starsIcon.className = 'fas fa-star stars-icon';
                        starsIcon.title = `${value.gh_stargazers_count} Stargazers`;
                        starsIcon.innerText = value.gh_stargazers_count;
                        projectIcons.appendChild(starsIcon);

                        // Add contributors
                        const usersIcon = document.createElement('i');
                        usersIcon.className = 'fas fa-user users-icon';
                        usersIcon.title = `${value.gh_num_contributors} Contributors`;
                        usersIcon.innerText = value.gh_num_contributors;
                        projectIcons.appendChild(usersIcon);

                        // Add commits
                        const codeIcon = document.createElement('i');
                        codeIcon.className = 'fas fa-code code-icon';
                        codeIcon.title = `${value.gh_num_commits} Commits`;
                        codeIcon.innerText = value.gh_num_commits;
                        projectIcons.appendChild(codeIcon);

                        // Add project icons to project card
                        projectCard.appendChild(projectIcons);
                        // END creating project icons

                        // START creating project description
                        const projectDescription = document.createElement('p');
                        projectDescription.className = 'project-description';
                        projectDescription.innerText = value.gh_description;
                        projectCard.appendChild(projectDescription);
                        // END creating project description

                        // START creating project topics
                        const cardSectionContainer = document.createElement('div');
                        cardSectionContainer.className = 'card-section-container';

                        const projectTopicsTitle = document.createElement('p');
                        projectTopicsTitle.className = 'project-topic-title';
                        projectTopicsTitle.innerText = 'Topics:';
                        cardSectionContainer.appendChild(projectTopicsTitle);

                        const projectTopics = document.createElement('div');
                        projectTopics.className = 'topic-container';

                        for (const topic of value.gh_topics) {
                            const topicLink = document.createElement('a');
                            topicLink.href = `https://github.com/search?q=${topic}&type=repositories`;
                            topicLink.className = 'project-topic-text';
                            topicLink.innerText = topic;
                            projectTopics.appendChild(topicLink);
                        }
                        cardSectionContainer.appendChild(projectTopics);
                        projectCard.appendChild(cardSectionContainer);
                        // END creating project topics

                        // START creating project issues
                        // if the issue dict is not empty
                        if (value.gh_issues_dict && Object.keys(value.gh_issues_dict).length > 0) {
                            const issuesCardSectionContainer = document.createElement('div');
                            issuesCardSectionContainer.className = 'card-section-container';

                            const projectIssuesTitle = document.createElement('p');
                            projectIssuesTitle.className = 'project-issue-title';
                            projectIssuesTitle.innerText = `Issues (${value.gh_num_open_issues} open):`;
                            issuesCardSectionContainer.appendChild(projectIssuesTitle);

                            const projectIssues = document.createElement('div');
                            projectIssues.className = 'issue-container';

                            for (const [issue_type, count] of Object.entries(value.gh_issues_dict)) {
                                const issueLink = document.createElement('a');
                                issueLink.href = `${value.repo_url}/issues?q=is%3Aissue+is%3Aopen+label%3A%22${issue_type}%22`;
                                issueLink.className = 'project-issue-text';
                                issueLink.innerText = `${issue_type} | ${count}`;
                                projectIssues.appendChild(issueLink);
                            }
                            issuesCardSectionContainer.appendChild(projectIssues);
                            projectCard.appendChild(issuesCardSectionContainer);
                        }
                        // END creating project issues

                        // projectCard.innerHTML = `
            //             <p class="project-description">{{ project.gh_description }}</p>

            // <div class="card-section-container">
            //     <p class="project-topic-title">Topics:</p>
            //     <div class="topic-container">
            //         {% for topic in project.gh_topics %}
            //         <a href="https://github.com/search?q={{ topic }}&type=repositories" class="project-topic-text">{{ topic }}</a>
            //         {% endfor %}
            //     </div>
            // </div>

            // {% if project.gh_issues_dict %}
            // <div class="card-section-container">
            //     <p class="project-issue-title">Issues ({{project.gh_num_open_issues}} open):</p>
            //     <div class="issue-container">
            //         {% for issue_type, count in project.gh_issues_dict.items() %}
            //         <a href="{{ project.repo_url }}/issues?q=is%3Aissue+is%3Aopen+label%3A%22{{ issue_type }}%22" class="project-issue-text">{{ issue_type }} | {{ count }} </a>
            //         {% endfor %}
            //     </div>
            // </div>
            // {% endif %}

            // {% if project.gh_date_of_last_commit %}
            // <div style="display: flex; justify-content: left; margin-top: 10px;">
            //     <div>
            //         <p class="last-commit-title">Last Commit:&nbsp;<a href="{{ project.repo_url }}/commits" class="last-commit-text">{{
            //                 project.gh_date_of_last_commit }}</a></p>
            //     </div>
            //     <div>
            //         <p class="last-commit-title">Last Merged PR:&nbsp;<a href="{{ project.repo_url }}//pulls?q=is%3Apr+is%3Aclosed" class="last-commit-text">{{
            //                 project.gh_date_of_last_commit }}</a></p>
            //     </div>
            // </div>
            // {% endif %}

            // <div class="card-bottom">
            //     <hr class="section-divider">
            //     <div class="pigeonhole-analysis-container">
            //         <h3 class="pigeonhole-analysis-title">Pigeonhole Analysis</h3>

            //         <div class="analysis-item">
            //             <i class="fas fa-user-check analysis-icon"></i>
            //             <p>New Contributor Score:</p>&nbsp;
            //             <div class="score-badge">{{ project.gh_new_contributor_score }}</div>
            //         </div>

            //         <div class="analysis-item">
            //             <i class="fas fa-heartbeat analysis-icon"></i>
            //             <p>Project Collaboration Health:</p>&nbsp;
            //             <div class="score-badge">{{ project.gh_collaboration_health }}</div>
            //         </div>
            //     </div>
            // </div>

                        // `;
                        // Add the project card to the project container
                        projectContainer.appendChild(projectCard);
                    }
                }
            });
    });

});