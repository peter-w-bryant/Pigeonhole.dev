/**
 * The function `createProjectCard` creates a project card element based on the provided project JSON
 * data.
 * @param projectJSON - The `projectJSON` parameter is an object that contains information about a
 * project. It has the following properties:
 * @returns a project card element (HTML div element) that is created based on the provided projectJSON
 * data.
 */
export function createProjectCard(projectJSON) {
    // Create a new project-square
    const projectCard = document.createElement('div');
    projectCard.className = 'project-square';

    // START creating project top (project name, contributing.md link, bug label, github link)
    const projectTop = document.createElement('div');
    projectTop.className = 'project-top';
    const projectName = document.createElement('a');
    projectName.href = projectJSON.repo_url;
    projectName.className = 'project-name';
    projectName.innerText = projectJSON.repo_name;
    projectTop.appendChild(projectName);

    // Create CONTRIBUTING.md link if it exists
    if (projectJSON.gh_contributing_url) {
        const contributingLink = document.createElement('a');
        contributingLink.className = 'project-label';
        contributingLink.href = projectJSON.gh_contributing_url;
        contributingLink.target = '_blank';
        const contributingText = document.createElement('p');
        contributingText.className = 'project-contributing-text';
        contributingText.innerText = 'CONTRIBUTING.md';
        const contributingIcon = document.createElement('i');
        contributingIcon.className = 'fas fa-file-code contributing-icon';
        contributingText.appendChild(contributingIcon);
        contributingLink.appendChild(contributingText);
        projectTop.appendChild(contributingLink);
    }

    // Create Bug Bounty link if it exists
    if (projectJSON.gh_has_bounty_label) {
        const bountyLink = document.createElement('a');
        bountyLink.className = 'project-label';
        bountyLink.href = projectJSON.gh_contributing_url;
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
    githubLink.href = projectJSON.repo_url;
    githubLink.target = '_blank';
    const githubIcon = document.createElement('i');
    githubIcon.className = 'fab fa-github github-icon';
    githubLink.appendChild(githubIcon);
    projectTop.appendChild(githubLink);

    // Add project top to the project card container
    projectCard.appendChild(projectTop);
    // END creating project top

    // START creating username container
    const usernameContainer = document.createElement('div');
    usernameContainer.className = 'username-container';
    const usernameLink = document.createElement('a');
    usernameLink.href = projectJSON.user_url;
    usernameLink.className = 'project-username';
    usernameLink.innerText = projectJSON.username;
    usernameContainer.appendChild(usernameLink);
    projectCard.appendChild(usernameContainer);
    // END creating username container

    // START creating project icons
    const projectIcons = document.createElement('div');
    projectIcons.className = 'project-icons';

    // Add watchers
    const viewsIcon = document.createElement('i');
    viewsIcon.className = 'fas fa-eye views-icon project-icon';
    viewsIcon.title = `${projectJSON.gh_watchers_count} Watchers`;
    projectIcons.appendChild(viewsIcon);
    const viewsText = document.createElement('p');
    viewsText.innerText = projectJSON.gh_watchers_count;
    projectIcons.appendChild(viewsText);

    // Add forks
    const forksIcon = document.createElement('i');
    forksIcon.className = 'fas fa-code-branch forks-icon project-icon';
    forksIcon.title = `${projectJSON.gh_forks_count} Forks`;
    projectIcons.appendChild(forksIcon);
    const forksText = document.createElement('p');
    forksText.innerText = projectJSON.gh_forks_count;
    projectIcons.appendChild(forksText);

    // Add stargazers
    const starsIcon = document.createElement('i');
    starsIcon.className = 'fas fa-star stars-icon project-icon';
    starsIcon.title = `${projectJSON.gh_stargazers_count} Stargazers`;
    projectIcons.appendChild(starsIcon);
    const starsText = document.createElement('p');
    starsText.innerText = projectJSON.gh_stargazers_count;
    projectIcons.appendChild(starsText);

    // Add contributors
    const usersIcon = document.createElement('i');
    usersIcon.className = 'fas fa-user users-icon project-icon';
    usersIcon.title = `${projectJSON.gh_num_contributors} Contributors`;
    projectIcons.appendChild(usersIcon);
    const usersText = document.createElement('p');
    usersText.innerText = projectJSON.gh_num_contributors;
    projectIcons.appendChild(usersText);

    // Add commits
    const codeIcon = document.createElement('i');
    codeIcon.className = 'fas fa-code code-icon project-icon';
    codeIcon.title = `${projectJSON.gh_num_commits} Commits`;
    projectIcons.appendChild(codeIcon);
    const codeText = document.createElement('p');
    codeText.innerText = projectJSON.gh_num_commits;
    projectIcons.appendChild(codeText);

    // Add project icons to project card
    projectCard.appendChild(projectIcons);
    // END creating project icons

    // START creating project description
    const projectDescription = document.createElement('p');
    projectDescription.className = 'project-description';
    projectDescription.innerText = projectJSON.gh_description;
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

    for (const topic of projectJSON.gh_topics) {
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
    if (projectJSON.gh_issues_dict && Object.keys(projectJSON.gh_issues_dict).length > 0) {
        const issuesCardSectionContainer = document.createElement('div');
        issuesCardSectionContainer.className = 'card-section-container';

        const projectIssuesTitle = document.createElement('p');
        projectIssuesTitle.className = 'project-issue-title';
        projectIssuesTitle.innerText = `Issues (${projectJSON.gh_num_open_issues} open):`;
        issuesCardSectionContainer.appendChild(projectIssuesTitle);

        const projectIssues = document.createElement('div');
        projectIssues.className = 'issue-container';

        for (const [issue_type, count] of Object.entries(projectJSON.gh_issues_dict)) {
            const issueLink = document.createElement('a');
            issueLink.href = `${projectJSON.repo_url}/issues?q=is%3Aissue+is%3Aopen+label%3A%22${issue_type}%22`;
            issueLink.className = 'project-issue-text';
            issueLink.innerText = `${issue_type} | ${count}`;
            projectIssues.appendChild(issueLink);
        }
        issuesCardSectionContainer.appendChild(projectIssues);
        projectCard.appendChild(issuesCardSectionContainer);
    }
    // END creating project issues

    // START creating project last commit
    if (projectJSON.gh_date_of_last_commit) {
        const lastCommitContainer = document.createElement('div');
        lastCommitContainer.style.display = 'flex';
        lastCommitContainer.style.justifyContent = 'left';
        lastCommitContainer.style.marginTop = '10px';
        const lastCommit = document.createElement('div');
        const lastCommitTitle = document.createElement('p');
        lastCommitTitle.className = 'last-commit-title';
        lastCommitTitle.innerText = 'Last Commit:';
        lastCommit.appendChild(lastCommitTitle);
        const lastCommitLink = document.createElement('a');
        lastCommitLink.href = `${projectJSON.repo_url}/commits`;
        lastCommitLink.className = 'last-commit-text';
        lastCommitLink.innerText = projectJSON.gh_date_of_last_commit;
        lastCommit.appendChild(lastCommitLink);
        lastCommitContainer.appendChild(lastCommit);


        // START creating project last merged PR
        const lastMerged = document.createElement('div');
        const lastMergedTitle = document.createElement('p');
        lastMergedTitle.className = 'last-commit-title';
        lastMergedTitle.innerText = 'Last Merged PR:';
        lastMerged.appendChild(lastMergedTitle);
        const lastMergedLink = document.createElement('a');
        lastMergedLink.href = `${projectJSON.repo_url}/pulls?q=is%3Apr+is%3Aclosed`;
        lastMergedLink.className = 'last-commit-text';
        lastMergedLink.innerText = projectJSON.gh_date_of_last_commit;
        lastMerged.appendChild(lastMergedLink);
        lastCommitContainer.appendChild(lastMerged);
        projectCard.appendChild(lastCommitContainer);

    }
    // END creating project last commit

    // START creating project bottom
    const cardBottom = document.createElement('div');
    cardBottom.className = 'card-bottom';
    const sectionDivider = document.createElement('hr');
    sectionDivider.className = 'section-divider';
    cardBottom.appendChild(sectionDivider);
    const pigeonholeAnalysisContainer = document.createElement('div');
    pigeonholeAnalysisContainer.className = 'pigeonhole-analysis-container';
    const pigeonholeAnalysisTitle = document.createElement('h3');
    pigeonholeAnalysisTitle.className = 'pigeonhole-analysis-title';
    pigeonholeAnalysisTitle.innerText = 'Pigeonhole Analysis';
    pigeonholeAnalysisContainer.appendChild(pigeonholeAnalysisTitle);

    const newContributorScore = document.createElement('div');
    newContributorScore.className = 'analysis-item';
    const newContributorIcon = document.createElement('i');
    newContributorIcon.className = 'fas fa-user-check analysis-icon';
    newContributorScore.appendChild(newContributorIcon);
    const newContributorText = document.createElement('p');
    newContributorText.innerText = 'New Contributor Score:';
    newContributorScore.appendChild(newContributorText);
    const newContributorScoreBadge = document.createElement('div');
    newContributorScoreBadge.className = 'score-badge';
    newContributorScoreBadge.innerText = projectJSON.gh_new_contributor_score;
    newContributorScore.appendChild(newContributorScoreBadge);
    pigeonholeAnalysisContainer.appendChild(newContributorScore);

    const collaborationHealth = document.createElement('div');
    collaborationHealth.className = 'analysis-item';
    const collaborationHealthIcon = document.createElement('i');
    collaborationHealthIcon.className = 'fas fa-heartbeat analysis-icon';
    collaborationHealth.appendChild(collaborationHealthIcon);
    const collaborationHealthText = document.createElement('p');
    collaborationHealthText.innerText = 'Project Collaboration Health:';
    collaborationHealth.appendChild(collaborationHealthText);
    const collaborationHealthBadge = document.createElement('div');
    collaborationHealthBadge.className = 'score-badge';
    collaborationHealthBadge.innerText = projectJSON.gh_collaboration_health;
    collaborationHealth.appendChild(collaborationHealthBadge);
    pigeonholeAnalysisContainer.appendChild(collaborationHealth);

    cardBottom.appendChild(pigeonholeAnalysisContainer);
    projectCard.appendChild(cardBottom);

    return projectCard;
}