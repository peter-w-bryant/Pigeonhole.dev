import { debounce } from './utils.js';
import { createProjectCard } from './createProjectCard.js';


// Global variables
let abortController = new AbortController(); // AbortController, used for aborting fetch requests
const datalist = document.getElementById('project-names'); // Datalist element, used for autocomplete

// Event listeners
document.getElementById('search-input').addEventListener('input', handleSearchForm);


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
function updateAutocompleteOptions(projectJSON) {
    // Create a new autocomplete option for each project
    for (const value of Object.values(projectJSON)) {
        const option = document.createElement('option');
        option.value = value.repo_name;
        option.text = value.username;
        datalist.appendChild(option);
    }
}

function updateProjectData(searchQuery) {
    console.log('Updating project data: updateProjectData()');
    const projectContainer = document.getElementById('project-container');
    projectContainer.innerHTML = '';

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

            // Clear all project cards
            datalist.innerHTML = '';

            updateAutocompleteOptions(data);

            // For each project in the full project list
            for (const value of Object.values(data)) {
                // If the project name contains the search query
                if (
                    value.repo_name.toLowerCase().includes(searchQuery.toLowerCase())
                ) {
                    // Create a new project card, and append it to the project container
                    const projectCard = createProjectCard(value);
                    projectContainer.appendChild(projectCard);
                }
            }

        })
        .catch((error) => {
            if (error.name === 'AbortError') {
                // Request was aborted, no action needed
            } else {
                // Handle other errors
                console.error(error);
            }
        });
}
