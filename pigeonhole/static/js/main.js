// Debounce function to limit the number of times a function is called
function debounce(func, delay) {
    let timeout;

    return function () {
        const context = this;
        const args = arguments;

        clearTimeout(timeout);

        timeout = setTimeout(() => {
            if (func) {
                func.apply(context, args);
            }
        }, delay);
    };
}

// Create a new AbortController for the current request
let abortController = new AbortController();

// Add event listeners to the select inputs
const topicSelect = document.getElementById('topic-select');
const issueSelect = document.getElementById('issue-select');

topicSelect.addEventListener('change', filterProjects);
issueSelect.addEventListener('change', filterProjects);

// Create a function to filter projects based on selected topics and issues
function filterProjects() {
    console.log('filtering projects');
    const searchQuery = document.getElementById('search-input').value;
    let selectedTopics = Array.from(topicSelect.selectedOptions).map(option => option.value);
    let selectedIssues = Array.from(issueSelect.selectedOptions).map(option => option.value);

    // Update the lists of selected topics and issues
    updateSelectedList(topicSelect, 'selected-topics-list');
    updateSelectedList(issueSelect, 'selected-issues-list');

    // Check if selectedTopics and selectedIssues are empty, and set them to null if necessary
    selectedTopics = selectedTopics.length === 0 ? null : selectedTopics;
    selectedIssues = selectedIssues.length === 0 ? null : selectedIssues;

    renderProjectCards(searchQuery, selectedTopics, selectedIssues);
}

function updateSelectedList(selectElement, listElementId) {
    const listElement = document.getElementById(listElementId);
    listElement.innerHTML = ''; // Clear the existing list items

    // Add new list items for each selected option
    Array.from(selectElement.selectedOptions).forEach(option => {
        const listItem = document.createElement('li');
        listItem.textContent = option.text;
        listElement.appendChild(listItem);
    });
}


// Add an event listener to the 'load' event to populate the select inputs
window.addEventListener('load', () => {
    fetch('api/static_data/projects.json')
        .then((response) => response.json())
        .then((data) => {
            const uniqueTopics = new Set();
            const uniqueIssues = new Set();

            // Collect unique topics and issues
            for (const [key, value] of Object.entries(data)) {
                for (const topic of value.gh_topics) {
                    uniqueTopics.add(topic);
                }

                for (const issueType of Object.keys(value.gh_issues_dict)) {
                    uniqueIssues.add(issueType);
                }
            }

            // Populate the topic select input
            for (const topic of uniqueTopics) {
                const option = document.createElement('option');
                option.value = topic;
                option.textContent = topic;
                topicSelect.appendChild(option);
            }

            // Populate the issue select input
            for (const issueType of uniqueIssues) {
                const option = document.createElement('option');
                option.value = issueType;
                option.textContent = issueType;
                issueSelect.appendChild(option);
            }

            updateSelectedList(topicSelect, 'selected-topics-list');
            updateSelectedList(issueSelect, 'selected-issues-list');
        });
});
// main.js
document.addEventListener('DOMContentLoaded', (event) => {
    const clearButtons = document.querySelectorAll('.clear-button');

    clearButtons.forEach(button => {
        button.addEventListener('click', clearSelected);
    });
});

function clearSelected(event) {
    // Identify which button was clicked
    const buttonId = event.target.id;

    // Determine which list to clear based on the button ID
    let listToClear;
    if (buttonId === 'clear-topics') {
        listToClear = document.getElementById('selected-topics-list');
    } else if (buttonId === 'clear-issues') {
        listToClear = document.getElementById('selected-issues-list');
    }

    // Clear the identified list
    if (listToClear) {
        listToClear.innerHTML = ''; // This removes all child elements in the list
    }

    console.log('clearing selected:', buttonId)
    // If you also need to clear the selections from the <select> elements
    if (buttonId === 'clear-topics') {
        const topicSelect = document.getElementById('topic-select');
        Array.from(topicSelect.options).forEach(option => option.selected = false);
        const selectedTopics = document.getElementById('selected-topics-list');
        //  Remove all list items from the selected topics list
        selectedTopics.innerHTML = '';

    } else if (buttonId === 'clear-issues') {
        const issueSelect = document.getElementById('issue-select');
        Array.from(issueSelect.options).forEach(option => option.selected = false);
        const selectedIssues = document.getElementById('selected-issues-list');
        //  Remove all list items from the selected issues list
        selectedIssues.innerHTML = '';
    }

    // You may need to call some function to update other parts of the UI or state
    // For example, re-render the project cards if they depend on these filters
    const searchQuery = document.getElementById('search-input').value;
    let selectedTopics = Array.from(topicSelect.selectedOptions).map(option => option.value);
    let selectedIssues = Array.from(issueSelect.selectedOptions).map(option => option.value);
    renderProjectCards(searchQuery, selectedTopics, selectedIssues);
}


function removeItem(event, itemValue) {
    // Handle removing the specific item both visually and logically
    event.target.parentNode.remove();
    // Further logic to unselect the item from the actual select element goes here
    const listItem = document.createElement('li');
    listItem.textContent = selectedValue;
    const removeButton = document.createElement('button');
    removeButton.classList.add('remove-item-button');
    removeButton.onclick = (event) => removeItem(event, selectedValue);
    listItem.appendChild(removeButton);
    document.getElementById('selected-topics-list').appendChild(listItem);
}




// Add event listeners for search inputs
document.getElementById('topic-search').addEventListener('input', handleTopicSearch);
document.getElementById('issue-search').addEventListener('input', handleIssueSearch);

function handleTopicSearch() {
    const searchTerm = this.value.toLowerCase();
    // const topicSelect = document.getElementById('topic-select');

    Array.from(topicSelect.options).forEach((option) => {
        const text = option.textContent.toLowerCase();
        option.selected = text.includes(searchTerm);
    });

}

function handleIssueSearch() {
    const searchTerm = this.value.toLowerCase();
    // const issueSelect = document.getElementById('issue-select');

    Array.from(issueSelect.options).forEach((option) => {
        const text = option.textContent.toLowerCase();
        option.selected = text.includes(searchTerm);
    });

}

// Add event listener to scroll and back-to-top button
window.addEventListener('scroll', handleScroll);
document.getElementById('back-to-top-button').addEventListener('click', scrollToTop);

function handleScroll() {
    const button = document.getElementById('back-to-top-button');
    if (window.scrollY > 200) {
        button.style.display = 'block'; // Show the button when scroll position is greater than 200px
    } else {
        button.style.display = 'none'; // Hide the button when scroll position is less than 200px
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Add smooth scrolling animation
    });
}

// Add event listener for search form
document.getElementById('search-input').addEventListener('input', handleSearchForm);

function handleSearchForm(e) {
    e.preventDefault();

    const searchQuery = document.getElementById('search-input').value;
    debounce(() => renderProjectCards(searchQuery), 300)();
}


function renderProjectCards(searchQuery, selectedTopics, selectedIssues) {
    console.log('rendering projects');
    const projectContainer = document.getElementById('project-container');
    projectContainer.innerHTML = '';

    // Abort the previous fetch request (if any)
    abortController.abort();

    // Create a new AbortController for the current request
    abortController = new AbortController();

    // Fetch data from 'api/static_data/projects.json'
    fetch('api/static_data/projects.json', {
        signal: abortController.signal,
    })
        .then((response) => response.json())
        .then((data) => {
            // Add all project names to the project names list 
            const datalist = document.getElementById('project-names');
            // Clear the datalist
            datalist.innerHTML = '';
            // for key value pairs in data
            for (const [key, value] of Object.entries(data)) {
                // Create a new option
                const option = document.createElement('option');
                // Set the option value to the project name
                option.value = value.repo_name;
                // Add "by username" to the option text but not the value
                option.text = value.username;

                // Add the option to the datalist
                datalist.appendChild(option);
            }

            // Data is a json object mapping github url to project dict
            // for key value pairs in data
            for (const [key, value] of Object.entries(data)) {
                if (
                    value.repo_name.toLowerCase().includes(searchQuery.toLowerCase()) &&
                    (!selectedTopics || selectedTopics.some(topic => value.gh_topics.includes(topic))) &&
                    (!selectedIssues || selectedIssues.some(issue => value.gh_issues_dict[issue] > 0))
                ) {
                    // If the project name contains the search query

                    // Create a new project-square
                    const projectCard = document.createElement('div');
                    projectCard.className = 'project-square';

                    // START creating project top (project name, contributing.md link, bug label, github link)
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
                        contributingIcon.className = 'fas fa-file-code contributing-icon';
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

                    // Add project top to the project card container
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

                    // START creating project last commit
                    if (value.gh_date_of_last_commit) {
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
                        lastCommitLink.href = `${value.repo_url}/commits`;
                        lastCommitLink.className = 'last-commit-text';
                        lastCommitLink.innerText = value.gh_date_of_last_commit;
                        lastCommit.appendChild(lastCommitLink);
                        lastCommitContainer.appendChild(lastCommit);


                        // START creating project last merged PR
                        const lastMerged = document.createElement('div');
                        const lastMergedTitle = document.createElement('p');
                        lastMergedTitle.className = 'last-commit-title';
                        lastMergedTitle.innerText = 'Last Merged PR:';
                        lastMerged.appendChild(lastMergedTitle);
                        const lastMergedLink = document.createElement('a');
                        lastMergedLink.href = `${value.repo_url}/pulls?q=is%3Apr+is%3Aclosed`;
                        lastMergedLink.className = 'last-commit-text';
                        lastMergedLink.innerText = value.gh_date_of_last_commit;
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
                    newContributorScoreBadge.innerText = value.gh_new_contributor_score;
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
                    collaborationHealthBadge.innerText = value.gh_collaboration_health;
                    collaborationHealth.appendChild(collaborationHealthBadge);
                    pigeonholeAnalysisContainer.appendChild(collaborationHealth);

                    cardBottom.appendChild(pigeonholeAnalysisContainer);
                    projectCard.appendChild(cardBottom);
                    // END creating project bottom

                    // Add the project card to the project container
                    projectContainer.appendChild(projectCard);
                }
            }

        })
        .catch((error) => {
            if (error.name === 'AbortError') {
                // Request was aborted, no action needed
            } else {
                // Handle other errors
            }
        });
}