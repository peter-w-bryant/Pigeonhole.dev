import { debounce } from './utils.js';
import { createProjectCard } from './createProjectCard.js';



// Global variables
let abortController = new AbortController(); // AbortController, used for aborting fetch requests
const datalist = document.getElementById('project-names');
const topicSelect = document.getElementById('topic-select');

// Event listeners
document.addEventListener('DOMContentLoaded', () => updateProjectData(''));
document.addEventListener('DOMContentLoaded', () => updateTopicSelect());
document.getElementById('search-input').addEventListener('input', handleSearchForm);
document.getElementById('topic-select').addEventListener('change', handleTopicSelect);

/**
 * The function `updateTopicSelect` fetches data from a JSON file, extracts unique topics from the
 * data, and dynamically populates a select element with options for each topic.
 */
function updateTopicSelect() {
    const topicSelect = document.getElementById('topic-select');
    const topicSet = new Set();
    fetch('api/static_data/projects.json')
        .then((response) => response.json())
        .then((data) => {
            for (const value of Object.values(data)) {
                for (const topic of value.gh_topics) {
                    topicSet.add(topic);
                }
            }
            // Create an option for each topic
            topicSelect.innerHTML = '';
            for (const topic of topicSet) {
                const option = document.createElement('option');
                option.value = topic;
                option.text = topic;
                topicSelect.appendChild(option);
            }
        });
}

function handleTopicSelect() {
    const searchQuery = document.getElementById('search-input').value;
    const selectedTopics = Array.from(topicSelect.selectedOptions).map(option => option.value);
    updateProjectData(searchQuery, selectedTopics);
}


/**
 * The handleSearchForm function prevents the form from submitting, gets the search query from the
 * input field, and debounces the updateProjectData function with a delay of 300 milliseconds.
 * @param e - The parameter `e` is an event object that represents the event that triggered the
 * function. In this case, it is the event object for the form submission event.
 */
function handleSearchForm(e) {
    e.preventDefault(); // Prevent the form from submitting
    const searchQuery = document.getElementById('search-input').value; // Get the search query
    debounce(() => updateProjectData(searchQuery), 300)(); // Debounce the updateProjectData function
}

/**
 * The function "updateAutocompleteOptions" creates autocomplete options for each project in a given
 * JSON object and appends them to a datalist element.
 * @param projectJSON - The `projectJSON` parameter is an object that contains information about
 * projects. Each project is represented by a key-value pair in the object, where the key is a unique
 * identifier for the project and the value is an object containing project details such as `repo_name`
 * and `username`.
 */
function updateAutocompleteOptions(projectJSON, searchQuery, selectedTopics = []) {
    // Create a new autocomplete option for each project
    datalist.innerHTML = '';
    for (const value of Object.values(projectJSON)) {
        if (!value.repo_name.toLowerCase().includes(searchQuery)
        ) {
            continue;
        }
        const option = document.createElement('option');
        option.value = value.repo_name;
        option.text = value.username;
        datalist.appendChild(option);
    }
}

function updateProjectData(searchQuery, selectedTopics = []) {
    console.log('Updating project data: updateProjectData()');
    searchQuery = searchQuery.trim().toLowerCase();
    const projectContainer = document.getElementById('project-container');
    const searchInput = document.getElementById('search-input');

    // Abort the previous fetch request (if any)
    if (abortController) {
        abortController.abort();
    }

    // Create a new AbortController for the current request
    abortController = new AbortController();

    // Fetch data from 'api/static_data/projects.json'
    fetch('api/static_data/projects.json', {
        signal: abortController.signal,
    })
        .then((response) => response.json())
        .then((data) => {

            updateAutocompleteOptions(data, searchQuery, selectedTopics);

            // For each project in the full project list
            let projectCount = 0;
            projectContainer.innerHTML = '';
            for (const value of Object.values(data)) {
                // If the project name contains the search query
                if (
                    value.repo_name.toLowerCase().includes(searchQuery) &&
                    selectedTopics.every(topic => value.gh_topics.includes(topic))
                ) {
                    // Create a new project card, and append it to the project container
                    const projectCard = createProjectCard(value);
                    projectContainer.appendChild(projectCard);
                    projectCount++;
                }
            }

            // If no projects were found
            if (projectCount === 0) {
                const noResults = document.createElement('p');
                noResults.textContent = 'No results found.';
                projectContainer.appendChild(noResults);
            }

            searchInput.scrollIntoView(); // Set focus on the search input
        })
        .catch((error) => {
            if (error.name === 'AbortError') {
                // Request was aborted, no action needed
            } else {
                // Handle other errors
            }
        });
}
